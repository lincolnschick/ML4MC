import numpy as np
import torch as th

from backend.ml4mc_env import ML4MCEnv
from backend.model import Model

class ModelRunner:
    """
    Class used to take actions according to a model in the ML4MC environment
    """
    def __init__(self, model: Model, ml4mc_env: ML4MCEnv):
        self._model = model
        self._ml4mc_env = ml4mc_env
    
    def run(self):
        """
        Takes actions according to the model until the agent dies or the user interrupts
        """
        self._ml4mc_env.update_action_shaping(self._model.extra_actions)
        obs, _, _, _ = self._ml4mc_env.step(0) # Get initial observations

        while True:
            # Process the action:
            #   - Add/remove batch dimensions
            #   - Transpose image (needs to be channels-last)
            #   - Normalize image
            obs = th.from_numpy(obs['pov'].transpose(2, 0, 1)[None].astype(np.float32) / 255)
            # Turn logits into probabilities
            probabilities = th.softmax(self._model.network(obs), dim=1)[0]
            # Into numpy
            probabilities = probabilities.detach().cpu().numpy()
            # Sample action according to the probabilities
            action = np.random.choice(self._ml4mc_env.action_list, p=probabilities)
            obs, _, done, _ = self._ml4mc_env.step(action)

            return done