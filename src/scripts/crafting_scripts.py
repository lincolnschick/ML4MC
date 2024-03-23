from scripts.script import Script
from GUI.gui import SCRIPT_FINISHED_MSG


class CraftToolScript(Script):
    def __init__(self, tool, resource_count, stick_count, ml4mc_env, notify_q):
        super().__init__(ml4mc_env, notify_q)
        self.tool = tool
        self.resource_count = resource_count
        self.stick_count = stick_count

    def run(self):
        """
        Craft the most powerful tool available based on the items in the inventory
        """
        self.center_agent_and_camera()
        
        # Look down to facilitate placing blocks beneath the agent
        obs = self.move_camera(89, 0)
        inventory = obs['inventory']
        
        # Figure out which tool we can craft
        tool_type = None
        if (inventory['iron_ingot'] >= self.resource_count
            or (inventory['iron_ore'] >= (self.resource_count - inventory['iron_ingot']) and self.smelt_iron())):
            tool_type = 'iron_'
        elif inventory['cobblestone'] >= self.resource_count:
            tool_type = 'stone_'
        elif inventory['planks'] >= self.resource_count or inventory['log']:
            if inventory['planks'] < self.resource_count: # We have logs but not planks
                self.take_action('craft:planks')
            inventory['planks'] -= self.resource_count # Use planks to craft tool, used for checking wood later
            tool_type = 'wooden_'
        else: # Can't craft any tool
            self.notify_q.put(SCRIPT_FINISHED_MSG)
            return

        # Check if we have enough sticks to craft the tool
        if inventory['stick'] < self.stick_count:
            if inventory['planks'] >= 2:
                self.take_action('craft:stick')
            elif inventory['log']:
                self.take_action('craft:planks')
                self.take_action('craft:stick')
            else: # We don't have enough wood to craft the tool
                self.notify_q.put(SCRIPT_FINISHED_MSG)
                return
        
        # Craft the item
        self.nearby_craft(tool_type + self.tool)

        # Look back up
        self.move_camera(-89, 0)
        self.notify_q.put(SCRIPT_FINISHED_MSG)

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

    def smelt_iron(self):
        """
        Smelt iron ore into iron ingots
        """
        obs = self.take_action('') # Get initial observation
        inventory = obs['inventory']
        iron_ingot_count = inventory['iron_ingot']

        # Try nearby smelt first in case we are near a furnace
        obs = self.take_action('nearbySmelt:iron_ingot')
        iron_needed = self.resource_count - iron_ingot_count
        if obs['inventory']['iron_ingot'] > iron_ingot_count:
            self.take_action('nearbySmelt:iron_ingot', times=iron_needed)
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
        
        self.take_action('nearbySmelt:iron_ingot', times=iron_needed)
        return True

class CraftSwordScript(CraftToolScript):
    def __init__(self, ml4mc_env, notify_q):
        # Swords require 2 of the resource and 1 stick
        super().__init__("sword", 2, 1, ml4mc_env, notify_q)

class CraftPickaxeScript(CraftToolScript):
    def __init__(self, ml4mc_env, notify_q):
        # Pickaxes require 3 of the resource and 2 sticks
        super().__init__("pickaxe", 3, 2, ml4mc_env, notify_q)
