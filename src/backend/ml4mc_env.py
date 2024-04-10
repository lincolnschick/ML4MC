import gym
import numpy as np
from multiprocessing import Queue
from time import sleep

from backend.config import Message

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
    def __init__(self, env, extra_actions=[], camera_angle=0, always_attack=False):
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
        
        if extra_actions:
            self._actions.extend(extra_actions)

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
    def __init__(self, obs_q: Queue, objective_q: Queue, restart_q: Queue, quit_q: Queue, pause_q: Queue, pov_q: Queue):
        self._display_pov = True # default
        self._display_pov_on_reset = True
        self._obs_q = obs_q
        self._objective_q = objective_q
        self._restart_q = restart_q
        self._quit_q = quit_q
        self._pause_q = pause_q
        self._pov_q = pov_q
        self._env = None
        self.action_list = None
        self._paused = False

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
        self.check_interrupt_queues()
        self.pause_agent() # Check if agent should be paused and wait if necessary

        if type(action) == str: # For scripted actions, we use the string format
            action = self.str_to_act(action)
            obs, reward, done, info = self._env.env.step(action) # Need to use the base env in this case
        else:
            obs, reward, done, info = self._env.step(action)
        
        if self._obs_q.empty(): # Avoid overloading the queue
            self._obs_q.put(obs) # Place data on the obs queue for the GUI

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
    
    def update_action_shaping(self, extra_actions: list):
        """
        Update the action shaping of the environment.
        """
        self._env = ActionShaping(self._env.env, extra_actions=extra_actions, always_attack=True)
        self.action_list = np.arange(self._env.action_space.n)
    
    def check_interrupt_queues(self):
        """
        Check the queues for new messages and raise corresponding exceptions.
        Passes control to the controller to handle the exceptions.
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
    
    def set_display_pov(self):
        """
        Update the display POV based on the current UI settings.
        This takes effect on the next environment reset.
        """
        if not self._pov_q.empty():
            while not self._pov_q.empty():
                self._display_pov_on_reset = self._pov_q.get()
        self._display_pov = self._display_pov_on_reset

    def pause_agent(self):
        """
        Function to handle the pause signal from the GUI.
        """
        if not self._paused and self._pause_q.empty():
            return
        self._paused = True

        msg = None
        while msg != Message.PLAY_AGENT: # Loop until the play message is received
            sleep(0.1)
            self.check_interrupt_queues() # Continue checking interrupt queues to maintain responsiveness
            if self._pause_q.empty():
                continue
            msg = self._pause_q.get()
        self._paused = False
        