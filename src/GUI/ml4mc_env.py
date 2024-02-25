import gym
import numpy as np
from multiprocessing import Queue, Pipe


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

class EpisodeFinishedException(Exception):
    pass

class RestartException(Exception):
    pass

class QuitException(Exception):
    pass

class ObjectiveChangedException(Exception):
    def __init__(self, objective):
        self.objective = objective

class ML4MCEnv:
    """
    Wrapper for the MineRL environment.
    All interaction with the environment should be done through this class.
    Failure to do so may result the UI becoming unresponsive and inconsistent behavior.
    """
    def __init__(self, display_pov: bool, to_emitter: Pipe, obs_q: Queue, objective_q: Queue, restart_q: Queue, quit_q: Queue):
        self._display_pov = display_pov
        self._obs_q = obs_q
        self._objective_q = objective_q
        self._restart_q = restart_q
        self._quit_q = quit_q
        self._to_emitter = to_emitter
        self._env = None
        self.action_list = None

    def start(self):
        """
        Launches the MineRL environment and sets up the action list.
        """
        # Set up environment with our custom environment
        self._env = gym.make('ML4MCSurvival-v0')
        self._env = ActionShaping(self._env, always_attack=True)

        # Enable using the interactor to join agent's world on LAN
        # This is fine to run even if the interactor is not needed
        self._env.make_interactive(port=5656)

        self.action_list = np.arange(self._env.action_space.n)

    def reset(self):
        """
        Resets the environment and returns the initial observation.
        """
        return self._env.reset()
    
    def step(self, action):
        """
        Wrapper for the step function of the MineRL environment.
        Handles communication with the GUI to ensure responsiveness.
        :raises: EpisodeFinishedException, RestartException, QuitException, ObjectiveChangedException
        """
        if not self._objective_q.empty():
            objective = None
            while not self._objective_q.empty():
                objective = self._objective_q.get()
            raise ObjectiveChangedException(objective)
        if not self._restart_q.empty():
            while not self._restart_q.empty():
                _ = self._restart_q.get()
            raise RestartException
        if not self._quit_q.empty():
            raise QuitException

        if type(action) == str: # For scripted actions, we use the string format
            action = self.str_to_act(action)
            obs, reward, done, info = self._env.env.step(action) # Need to use the base env in this case
        else:
            obs, reward, done, info = self._env.step(action)
        
        self._obs_q.put(obs.copy())            # Place data on the obs queue for the GUI
        # self._to_emitter.send("obs")    # Send data to emitter to tell which signal to send

        if done:
            raise EpisodeFinishedException
        if self._display_pov:
            self._env.render()
        return obs, reward, done, info
    
    def str_to_act(self, actions):
        """
        Simplifies specifying actions for the scripted part of the agent.
        Some examples for a string with a single action:
            'craft:planks'
            'camera:[10,0]'
            'attack'
            'jump'
            ''
        There should be no spaces in single actions, as we use spaces to separate actions with multiple "buttons" pressed:
            'attack sprint forward'
            'forward camera:[0,10]'

        :param env: base MineRL environment.
        :param actions: string of actions.
        :return: dict action, compatible with the base MineRL environment.
        """
        act = self._env.unwrapped.action_space.noop()
        for action in actions.split():
            if ":" in action:
                k, v = action.split(':')
                if k == 'camera':
                    act[k] = eval(v)
                else:
                    act[k] = v
            else:
                act[action] = 1
        return act