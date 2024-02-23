import numpy as np
import torch as th
import torch.nn as nn
from ml4mc_env import ML4MCEnv


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


class ModelRunner:
    """
    Class used to take actions according to a model in the ML4MC environment
    """
    def __init__(self, model: str, ml4mc_env: ML4MCEnv):
        self._network = NatureCNN((3, 64, 64), 7)
        self._model = model
        self._ml4mc_env = ml4mc_env
    
    def run(self):
        """
        Takes actions according to the model until the agent dies or the user interrupts
        """
        self._network.load_state_dict(th.load(self._model.get_filepath(), map_location=th.device("cpu")))
        obs, _, _, _ = self._ml4mc_env.step(0) # Get initial observations

        while True:
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
            action = np.random.choice(self._ml4mc_env.action_list, p=probabilities)
            obs, _, done, _ = self._ml4mc_env.step(action)

            return done