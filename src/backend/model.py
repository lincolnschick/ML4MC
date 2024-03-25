import os
from backend.ml4mc_env import ML4MCEnv
from abc import ABC, abstractmethod


class Model(ABC):
    """
    Base class for behavioral cloning and reinforcement learning models.
    """
    def __init__(self, ml4mc_env: ML4MCEnv, name: str, extra_actions: list = []):
        """
        :param ml4mc_env: environment to run the model in
        :param name: name of the model file
        :param extra_actions: additional actions to incorporate into the ActionShaping/environment
        """
        self._ml4mc_env = ml4mc_env
        self._name = name
        self.extra_actions = extra_actions

    def get_file_path(self):
        """
        Get the file path of the model
        """
        return os.path.join(os.path.dirname(__file__), "models", self._name)

    @abstractmethod
    def get_next_action(self, obs):
        """
        Uses the current model to predict the best action to take given the observations
        """
        pass
    
    def run(self):
        """
        Takes actions according to the model until the agent dies or the user interrupts
        """
        self._ml4mc_env.update_action_shaping(self.extra_actions)
        obs, _, _, _ = self._ml4mc_env.step(0) # Get initial observations

        while True:
            action = self.get_next_action(obs)
            obs, _, _, _ = self._ml4mc_env.step(action)
