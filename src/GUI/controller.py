"""
Author: Adair Torres, Lincoln Schick
Description:
    AgentController object to handle interaction between GUI and Models.
    Loads environments and models accordingly.

    TODO:
        - Implement progress tracking for model goals.
        - Implement pausing / resuming actions for models.
        - Implement recording model action frames.
        - Implement toggling of individual scripts.
Last Modified: 2-6-2024
"""

import minerl
import gym
import os
import torch as th
import numpy as np
import torch.nn as nn

from model import Model
from minerl.herobraine.env_specs.ml4mc_survival_specs import ML4MCSurvival

class NatureCNN(nn.Module):
    """
    CNN from DQN nature paper:
        Mnih, Volodymyr, et al.
        "Human-level control through deep reinforcement learning."
        Nature 518.7540 (2015): 529-533.

    :param input_shape: A three-item tuple telling image dimensions in (C, H, W)
    :param output_dim: Dimensionality of the output vector
    """

    def __init__(self, input_shape, output_dim):
        super().__init__()
        n_input_channels = input_shape[0]
        self.cnn = nn.Sequential(
            nn.Conv2d(n_input_channels, 32, kernel_size=8, stride=4, padding=0),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=4, stride=2, padding=0),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=0),
            nn.ReLU(),
            nn.Flatten(),
        )

        # Compute shape by doing one forward pass
        with th.no_grad():
            n_flatten = self.cnn(th.zeros(1, *input_shape)).shape[1]

        self.linear = nn.Sequential(
            nn.Linear(n_flatten, 512),
            nn.ReLU(),
            nn.Linear(512, output_dim)
        )

    def forward(self, observations: th.Tensor) -> th.Tensor:
        return self.linear(self.cnn(observations))


class ActionShaping(gym.ActionWrapper):
    """
    The default MineRL action space is the following dict:

    Dict(attack:Discrete(2),
         back:Discrete(2),
         camera:Box(low=-180.0, high=180.0, shape=(2,)),
         craft:Enum(crafting_table,none,planks,stick,torch),
         equip:Enum(air,iron_axe,iron_pickaxe,none,stone_axe,stone_pickaxe,wooden_axe,wooden_pickaxe),
         forward:Discrete(2),
         jump:Discrete(2),
         left:Discrete(2),
         nearbyCraft:Enum(furnace,iron_axe,iron_pickaxe,none,stone_axe,stone_pickaxe,wooden_axe,wooden_pickaxe),
         nearbySmelt:Enum(coal,iron_ingot,none),
         place:Enum(cobblestone,crafting_table,dirt,furnace,none,stone,torch),
         right:Discrete(2),
         sneak:Discrete(2),
         sprint:Discrete(2))

    It can be viewed as:
         - buttons, like attack, back, forward, sprint that are either pressed or not.
         - mouse, i.e. the continuous camera action in degrees. The two values are pitch (up/down), where up is
           negative, down is positive, and yaw (left/right), where left is negative, right is positive.
         - craft/equip/place actions for items specified above.
    So an example action could be sprint + forward + jump + attack + turn camera, all in one action.

    This wrapper makes the action space much smaller by selecting a few common actions and making the camera actions
    discrete. You can change these actions by changing self._actions below. That should just work with the RL agent,
    but would require some further tinkering below with the BC one.
    """
    def __init__(self, env, camera_angle=10, always_attack=False):
        super().__init__(env)

        self.camera_angle = camera_angle
        self.always_attack = always_attack
        self._actions = [
            [('attack', 1)],
            [('forward', 1)],
            [('forward', 1), ('jump', 1)],
            [('camera', [-self.camera_angle, 0])],
            [('camera', [self.camera_angle, 0])],
            [('camera', [0, self.camera_angle])],
            [('camera', [0, -self.camera_angle])],
        ]

        self.actions = []
        for actions in self._actions:
            act = self.env.action_space.noop()
            for a, v in actions:
                act[a] = v
            if self.always_attack:
                act['attack'] = 1
            self.actions.append(act)

        self.action_space = gym.spaces.Discrete(len(self.actions))

    def action(self, action):
        return self.actions[action]

class AgentController():
    def __init__(self, dirname, obs_q, objective_q):
        """
        Description:
            Construction for AgentController class. Contains member variables
            for tracking current environment, goal progress, queues for communication with GUI, 
            and state of the run (i.e. paused / running).
        """
        self._DIRNAME = dirname
        self._env = None
        self._currentModel = None
        self._progress = 0           # For tracking goal progress
        self._paused = False         # Receiving signal to halt actions from the GUI
        self._obs_q = obs_q
        self._objective_q = objective_q

        self._modelDict = {}
        
        modelsList = [("diamond_model_placeholder", "Obtain Diamond"),
                      ("iron_model.pth", "Obtain Iron"),
                      ("surive_model_placeholder", "Survive"),
                      ("wood_model.pth", "Gather Wood"),
                      ("stone_model_placeholder", "Gather Stone"),
                      ("enemies_model_placeholder", "Defeat Enemies")]
        
        for pair in modelsList:
            modelPath = os.path.join(self._DIRNAME, "models", pair[0])
            newModel = Model(pair[0], pair[1], modelPath)
            self._modelDict[newModel.get_objective()] = newModel
        
        # Set the current model to the default
        self._currentModel = self._modelDict["Obtain Diamond"]
        self._network = NatureCNN((3, 64, 64), 7)
        
        # Initialize and register custom environments
        ml4mcSurvival = ML4MCSurvival()
        ml4mcSurvival.register()
    
    def run(self):
        """
        Description:
            Main loop for the agent controller, which is run as a separate process.
        """
        # Update objective if necessary
        self.handle_objective_queue()
        self._network.load_state_dict(th.load(self._currentModel.get_filepath(), map_location=th.device("cpu")))

        # Test agent on a different environment
        self._env = gym.make('ML4MCSurvival-v0')
        self._env = ActionShaping(self._env, always_attack=True)

        # Enable using the interactor to join agent's world on LAN
        # self._env.make_interactive(port=5656)

        num_actions = self._env.action_space.n
        action_list = np.arange(num_actions)

        # Continue looping until process terminates by user closing the GUI
        while True:
            # Set up environment from specification
            obs = self._env.reset()

            # Loop through the environment until the agent dies or the user wishes to restart (TODO)
            done = False
            while not done:
                # Check for messages from the GUI to update the current objective
                self.handle_objective_queue()

                # Process the action:
                #   - Add/remove batch dimensions
                #   - Transpose image (needs to be channels-last)
                #   - Normalize image
                obs = th.from_numpy(obs['pov'].transpose(2, 0, 1)[None].astype(np.float32) / 255)
                # Turn logits into probabilities
                probabilities = th.softmax(self._network(obs), dim=1)[0]
                # Into numpy
                probabilities = probabilities.detach().cpu().numpy()
                # Sample action according to the probabilities
                action = np.random.choice(action_list, p=probabilities)
                obs, _, done, _ = self._env.step(action)

                # Render new observation
                self._env.render()

    def handle_objective_queue(self):
        """
        Description:
            Function to handle items in the objective queue, used to update the current objective and model.
        """
        while not self._objective_q.empty():
            objective = self._objective_q.get()
            self._currentModel = self._modelDict[objective]
            self._network.load_state_dict(th.load(self._currentModel.get_filepath(), map_location=th.device("cpu")))
    
    def reset_environment(self):
        """
        Description:
            Reset the current environment.
        """
        self._env.reset()
        return