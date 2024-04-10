"""
Convert scripts folder into a submodule
for easier imports across directories.
"""

from backend.scripts.mine_to_surface import MineToSurfaceScript
from backend.scripts.collect_diamonds import CollectDiamondsScript
from backend.scripts.gather_stone import GatherStoneScript
from backend.scripts.crafting_scripts import CraftSwordScript, CraftPickaxeScript
from backend.scripts.place_torch import PlaceTorchScript
from backend.scripts.shelter import ShelterScript