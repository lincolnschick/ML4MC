"""
Author: Adair Torres
Description:
    Model object file to represent individual models.
Last Modified: 1-28-2024
"""

import os
import torch.nn as nn
import torch as th

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

class Model:
    def __init__(self, name: str, network: NatureCNN, extra_actions: list = []):
        self._name = name
        self._FILEPATH = os.path.join(os.path.dirname(__file__), "models", name)
        self.network = network
        self.network.load_state_dict(th.load(self._FILEPATH, map_location=th.device("cpu")))
        self.extra_actions = extra_actions

class IronModel(Model):
    def __init__(self):
        super().__init__("iron_model.pth", NatureCNN((3, 64, 64), 7))
    
class WoodModel(Model):
    def __init__(self):
        super().__init__(
            "wood_model.pth", NatureCNN((3, 64, 64), 7))

class StoneModel(Model):
    def __init__(self):
        super().__init__(
            "stone_model.pth",
            NatureCNN((3, 64, 64), 15),
            [
                [('craft', 'planks')],
                [('craft', 'stick')],
                [('craft', 'crafting_table')],
                [('place', 'crafting_table')],
                [('nearbyCraft', 'wooden_pickaxe')],
                [('nearbyCraft', 'stone_pickaxe')],
                [('equip', 'wooden_pickaxe')],
                [('equip', 'stone_pickaxe')]
            ])
