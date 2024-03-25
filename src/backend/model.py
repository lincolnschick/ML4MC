import os
from backend.ml4mc_env import ML4MCEnv
from abc import ABC, abstractmethod


class Model(ABC):
    def __init__(self, ml4mc_env: ML4MCEnv, name: str, extra_actions: list = []):
        self._ml4mc_env = ml4mc_env
        self._name = name
        self.extra_actions = extra_actions

    def get_file_path(self):
        return os.path.join(os.path.dirname(__file__), "models", self._name)

    @abstractmethod
    def get_next_action(self, obs):
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
