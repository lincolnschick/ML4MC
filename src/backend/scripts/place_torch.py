from backend.scripts.script import Script
from backend.config import Message

PICKAXES = ['iron_pickaxe', 'stone_pickaxe', 'wooden_pickaxe']

class PlaceTorchScript(Script):
    def __init__(self, ml4mc_env, notify_q):
        super().__init__(ml4mc_env, notify_q)

    def run(self):
        """
        Craft a torch using a stick and coal / charcoal based on the items in the inventory
        """

        self.center_agent_and_camera()

        # Look down to facilitate placing blocks beneath the agent
        obs = self.move_camera(89, 0)
        inventory = obs['inventory']

        # Save initial height to mine any placed blocks later
        initial_height = int(obs['location_stats']['ypos'])

        HAVE_COAL = (inventory['coal'] >= 1)

        if not inventory['torch'] >= 1:
            # Check for sticks first, we don't want to go through crafting and/or
            # placing a furnace if we don't have a stick leftover to finish.
            if not inventory['stick'] >= 1:
                if inventory['planks'] >= 2:
                    self.take_action('craft:stick')
                elif (inventory['log'] >= 1 and HAVE_COAL) or (inventory['log'] >= 2 and not HAVE_COAL):
                    # If we don't have sticks or coal, we need at least 2 logs. If have coal but not sticks, we need just one log.
                    self.take_action('craft:planks')
                    self.take_action('craft:stick')
                else: # We don't have enough wood to craft a torch
                    self.notify_q.put(Message.SCRIPT_FINISHED)
                    return

            if not HAVE_COAL:
                if inventory['log'] >= 1:
                    self.smelt_coal()
                    self.mine_placed_blocks(initial_height)
                else:
                    self.notify_q.put(Message.SCRIPT_FINISHED)
                    return

            self.take_action("craft:torch")
        
        self.take_action('sneak place:' + 'torch', times=5)
        # Tilt camera upwards so we don't immediately break the torch.
        obs = self.move_camera(-90, 0)

        self.notify_q.put(Message.SCRIPT_FINISHED)
        return

    def jump_and_place(self, item):
        """
        Jump and place the specified item
        :param item: str, the item to place
        """
        self.take_action('attack') # Break possible grass beneath the agent

        # Jump and place the item below the agent
        self.take_action('jump')
        self.take_action('sneak place:' + item, times=5)

    def craft_crafting_table(self):
        """
        Craft a crafting table using available resources
        :param inventory: dict, the inventory of the agent
        :return: bool, True if a crafting table was created, False otherwise
        """
        obs = self.take_action('')
        inventory = obs['inventory']
        if inventory['planks'] < 4:
            if not inventory['log']:
                return False
            self.take_action('craft:planks')
        self.take_action('craft:crafting_table')
        return True

    def nearby_craft(self, item):
        """
        Craft an item using nearby crafting table
        :param item: str, the item to craft
        :return: bool, True if the item was crafted, False otherwise
        """
        obs = self.take_action('') # Get initial observation
        inventory = obs['inventory']
        item_count = inventory[item]

        # Try nearby craft first in case we are near a crafting table
        obs = self.take_action('nearbyCraft:' + item)
        obs = self.take_action('', times=5) # Wait for crafting to finish
        if obs['inventory'][item] > item_count:
            return True
        
        # Check if we have a crafting table in the inventory or can craft one
        if not inventory['crafting_table'] and not self.craft_crafting_table():
            return False
    
        self.jump_and_place('crafting_table')
        obs = self.take_action('nearbyCraft:' + item)
        obs = self.take_action('', times=5) # Wait for crafting to finish
        return obs['inventory'][item] > item_count
    
    def smelt_coal(self):
        """
        Smelt logs into coal (charcoal)
        """
        obs = self.take_action('') # Get initial observation
        inventory = obs['inventory']
        coal_count = inventory['coal']

        # Try nearby smelt first in case we are near a furnace
        obs = self.take_action('nearbySmelt:coal')
        if obs['inventory']['coal'] > coal_count:
            return True
        
        # Check if we have a furnace in the inventory or can craft one
        if inventory['furnace']:
            self.jump_and_place('furnace')
        elif inventory['cobblestone'] >= 8:
            if not self.nearby_craft('furnace'):
                return False
            self.jump_and_place('furnace')
        else:
            return False
        
        self.take_action('nearbySmelt:coal')
        return True
    
    def mine_placed_blocks(self, initial_height):
        obs = self.take_action('')
        inventory = obs['inventory']
        print("initial height:", initial_height)
        print("current height:", obs['location_stats']['ypos'])
        # Equip pickaxe if available
        for pickaxe in PICKAXES:
            if not inventory[pickaxe]:
                continue
            obs = self.take_action('equip:' + pickaxe)
            break

        # Mine any blocks placed to craft the tool
        while int(obs['location_stats']['ypos']) > initial_height:
            obs = self.take_action('attack')

    