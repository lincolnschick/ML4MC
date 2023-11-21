import numpy as np
import torch as th
from torch import nn
import gym
import minerl
from minerl.herobraine.env_specs.stone_collection_specs import StoneCollection
import logging


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
            # Actions below not needed for treechop
            # [('back', 1)],
            # [('left', 1)],
            # [('right', 1)],
            # [('jump', 1)],
            # [('forward', 1), ('attack', 1)],
            # [('craft', 'planks')],
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
    
# Parameters:
TRAIN_MODEL_NAME = 'behavioral_cloning.pth'  # name to use when saving the trained agent.
TEST_MODEL_NAME = 'behavioral_cloning.pth'  # name to use when loading the trained agent.

TEST_EPISODES = 5  # number of episodes to test the agent for.
MAX_TEST_EPISODE_LEN = 5000  # 18k is the default for MineRLObtainDiamond.
STONECOLLECT_STEPS = 3000  # number of steps to run BC for in evaluations.

def test():
    network = NatureCNN((3, 64, 64), 7)
    network.load_state_dict(th.load(TEST_MODEL_NAME, map_location=th.device("cpu")))

    # Test custom environment
    # abs_STONE = StoneCollection()
    # abs_STONE.register() # Register with gym
    env = gym.make('StoneCollection-v0')
    env = ActionShaping(env, always_attack=True)

    num_actions = env.action_space.n
    action_list = np.arange(num_actions)

    for episode in range(TEST_EPISODES):
        obs = env.reset()
        done = False
        total_reward = 0
        steps = 0

        # BC part to get some logs:
        for i in range(STONECOLLECT_STEPS):
            # Process the action:
            #   - Add/remove batch dimensions
            #   - Transpose image (needs to be channels-last)
            #   - Normalize image
            obs = th.from_numpy(obs['pov'].transpose(2, 0, 1)[None].astype(np.float32) / 255)
            # Turn logits into probabilities
            probabilities = th.softmax(network(obs), dim=1)[0]
            # Into numpy
            probabilities = probabilities.detach().cpu().numpy()
            # Sample action according to the probabilities
            action = np.random.choice(action_list, p=probabilities)
        
            obs, reward, done, info = env.step(action)
            env.render() # Display state locally
            total_reward += reward
            steps += 1
            if done:
                break

        print(f'Episode #{episode + 1} reward: {total_reward}\t\t episode length: {steps}')
    env.close()

test()