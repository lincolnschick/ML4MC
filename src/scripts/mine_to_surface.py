import minerl
import gym
from scripts.script import Script, secs_to_ticks


# Amount of time we should mine for each pickaxe type
# Padded based on tests to account for lag and mining dirt/sand at surface
MINING_SECS_BY_PICKAXE = {
    'iron_pickaxe': 1.0,
    'stone_pickaxe': 1.2,
    'wooden_pickaxe': 1.45,
}

def is_underground(prev_inventory, obs, pickaxe):
    """
    Mines up until we can see the sky if the agent is using its fist or until the inventory does not change if the agent has a pickaxe.
    The inventory check is more accurate due to tree coverage.
    :param prev_inventory: dict, previous inventory of the agent
    :param obs: dict, current observation
    :param pickaxe: string, name of the pickaxe the agent is using
    :return: bool, True if the agent is underground, False otherwise
    """
    if pickaxe and prev_inventory == obs['inventory']:
        return False
    return not obs['location_stats']['can_see_sky']

def is_mining_dirt(prev_inventory, obs):
    """
    Checks if the agent is mining dirt, used to handle the iron pickaxe bug
    :param prev_inventory: dict, previous inventory of the agent
    :param obs: dict, current observation
    :return: bool, True if the agent is mining dirt, False otherwise
    """
    if not prev_inventory:
        return False # This would mean we haven't mined anything yet
    prev_dirt = prev_inventory['dirt'] if 'dirt' in prev_inventory else 0
    cur_dirt = obs['inventory']['dirt'] if 'dirt' in obs['inventory'] else 0
    if cur_dirt - prev_dirt >= 3: # We will likely be mining dirt until we reach the surface
        return True
    return False

class MineToSurfaceScript(Script):
    def __init__(self, ml4mc_env):
        super().__init__(ml4mc_env)

    def equip_best_pickaxe(self, obs):
        """
        Equips the most efficient pickaxe we have and return the observation and time to mine a block based on this
        :param obs: dict, current observation
        :return: dict, observation after equipping the best pickaxe, name of the pickaxe, and time to mine a block
        """
        inventory = obs['inventory']
        for pickaxe, secs in MINING_SECS_BY_PICKAXE.items():
            if pickaxe in inventory and inventory[pickaxe] > 0:
                obs = self.take_action(f'equip:{pickaxe}')
                return obs, pickaxe, secs_to_ticks(secs)
        
        # We have no pickaxes, so return default values for bare hand
        return obs, None, secs_to_ticks(8)

    def run(self):
        """
        Brings the agent from underground to the surface by mining in a staircase pattern
        :return: None
        """
        self.center_agent_and_camera()

        # Run and jump forward for 2 seconds to approach a wall if we are in the middle of a cave
        obs = self.take_action('jump forward sprint', secs_to_ticks(2))

        # Look straight up to prepare for loop
        obs = self.move_camera(-90, 0)

        # Equip best pickaxe we have and set time to mine a block    
        obs, pickaxe, mine_ticks = self.equip_best_pickaxe(obs)

        # Set up variables for loop
        prev_inventory = None
        prev_pos = None
        handled_iron_bug = False
        while is_underground(prev_inventory, obs, pickaxe):
            cur_pos = (obs['location_stats']['xpos'], obs['location_stats']['zpos'])
            # Check if pickaxe has broken
            if pickaxe and obs['equipped_items']['mainhand']['type'] != pickaxe:
                # Equip best pickaxe we have and update time to mine a block
                obs, pickaxe, mine_ticks = self.equip_best_pickaxe(obs)
            elif prev_pos == cur_pos: # Check if we are stuck (and we know its not because our pickaxe broke)
                mine_ticks *= 2 # Double time to mine a block (could be facing ore, wood, etc.)
            prev_pos = cur_pos

            # Correction for iron pickaxe bug
            if pickaxe == 'iron_pickaxe' and not handled_iron_bug and is_mining_dirt(prev_inventory, obs):
                mine_ticks += 6 # Increase time to mine a block
                handled_iron_bug = True

            # Update previous inventory
            prev_inventory = obs['inventory']

            # Mine block above agent
            obs = self.take_action('attack', mine_ticks)

            # Look at next block (pitch becomes -60)
            obs = self.move_camera(30, 0)

            # Mine next block
            obs = self.take_action('attack', mine_ticks)

            # Look straight at final block (pitch becomes 0)
            obs = self.move_camera(60, 0)

            # Mine final block
            obs = self.take_action('attack', mine_ticks)

            # Jump and move forward to move onto next stair level
            obs = self.take_action('jump')
            obs = self.take_action('sprint forward', secs_to_ticks(0.75))

            # Look straight up (pitch goes from 0 to -90)
            obs = self.move_camera(-90, 0)

        # Return camera to parallel with the ground. The agent will be looking straight up when the loop ends
        obs = self.move_camera(90, 0)

        # If we exited because of the sky only, we need to get up one final level
        if obs['inventory'] != prev_inventory:
            # Jump and move forward to move onto final level
            obs = self.take_action('jump')
            obs = self.take_action('sprint forward', secs_to_ticks(0.75))

        # We will now loop until the user changes scripts/objectives
        while True:
            self.take_action('')