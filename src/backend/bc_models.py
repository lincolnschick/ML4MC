import torch.nn as nn
import torch as th
import numpy as np
from backend.ml4mc_env import ML4MCEnv
from backend.model import Model


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


class BCModel(Model):
    """
    Base class for behavioral cloning models.
    """
    def __init__(self, ml4mc_env: ML4MCEnv, name: str, network: NatureCNN, extra_actions: list = []):
        super().__init__(ml4mc_env, name, extra_actions)
        self.network = network
        self.network.load_state_dict(th.load(self.get_file_path(), map_location=th.device("cpu")))
    
    def get_next_action(self, obs):
        # Process the action:
        #   - Add/remove batch dimensions
        #   - Transpose image (needs to be channels-last)
        #   - Normalize image
        obs = th.from_numpy(obs['pov'].transpose(2, 0, 1)[None].astype(np.float32) / 255)
        # Turn logits into probabilities
        probabilities = th.softmax(self.network(obs), dim=1)[0]
        # Into numpy
        probabilities = probabilities.detach().cpu().numpy()
        # Sample action according to the probabilities
        return np.random.choice(self._ml4mc_env.action_list, p=probabilities)
        

class IronModel(BCModel):
    """"
    Class for the iron model, whose goal is to mine iron and craft an iron pickaxe.
    """
    def __init__(self, ml4mc_env: ML4MCEnv):
        super().__init__(
            ml4mc_env,
            "iron_model.pth",
            NatureCNN((3, 64, 64), 18),
            [
                [('craft', 'planks')],
                [('craft', 'stick')],
                [('craft', 'crafting_table')],
                [('craft', 'furnace')],
                [('place', 'crafting_table')],
                [('place', 'furnace')],
                [('nearbyCraft', 'stone_pickaxe')],
                [('nearbyCraft', 'iron_pickaxe')],
                [('nearbySmelt', 'iron_ingot')],
                [('equip', 'stone_pickaxe')],
                [('equip', 'iron_pickaxe')]
            ])
    
class WoodModel(BCModel):
    """
    Class for the wood model, whose goal is to gather wood (it cannot craft anything).
    """
    def __init__(self, ml4mc_env: ML4MCEnv):
        super().__init__(ml4mc_env, "wood_model.pth", NatureCNN((3, 64, 64), 7))

class StoneModel(BCModel):
    """
    Class for the stone model, whose goal is to gather stone and craft a stone pickaxe.
    """
    def __init__(self, ml4mc_env: ML4MCEnv):
        super().__init__(
            ml4mc_env,
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
