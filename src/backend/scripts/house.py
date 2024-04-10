from backend.scripts.script import Script
from backend.config import Message


class HouseScript(Script):
    def __init__(self, ml4mc_env, notify_q):
        super().__init__(ml4mc_env, notify_q)
    
    def run(self):
        """
        Create a house to protect the agent from mobs.
        Assumes the agent has the necessary resources in the inventory.
        """
        self.center_agent_and_camera()
        
        # Look down to facilitate placing blocks below the agent
        self.move_camera(55, 0)

        # Craft necessary items and place them in the home in a row
        self.repeat(self.craft_item, 'planks', times=12) # Needed for walls
        self.craft_item('crafting_table', delay=10)
        self.take_action('place:crafting_table')
        self.nearby_craft('chest')
        self.nearby_craft('furnace')
        self.take_action('sneak right', times=15) # Move to the right of the crafting table
        self.take_action('place:furnace')
        self.repeat(self.nearby_smelt, 'stone', times=33) # Needed for slab ceiling
        self.repeat(self.nearby_smelt, 'glass', times=7) # Needed for windows
        self.repeat(self.nearby_craft, 'stone_slab', times=11) # Needed for ceiling
        self.take_action('sneak right', times=15) # Move to the right of the furnace
        self.take_action('place:chest')
        self.delay(10) # Allow chest to render

        # Get in position to place outer walls
        self.take_action('forward', times=5)
        self.take_action('sneak forward jump', times=15) # Get on top of the chest
        self.delay(10)
        self.center_agent_and_camera()
        self.move_camera(89, -90) # Turn left and look down
        self.take_action('sneak forward', times=40)
        self.sneak_to_edge_and_jump() # Get to the edge of the crafting table

        # Place wall left of the row of items
        self.place_plank_pillar()
        self.move_camera(0, -90) # Turn left
        self.sneak_to_edge_and_jump()
        self.place_window_pillar()
        self.sneak_to_edge_and_jump()
        self.place_plank_pillar()
        self.sneak_to_edge_and_jump()
        self.place_log_pillar()

        # Place wall behind row of items
        self.move_camera(0, -90)
        self.sneak_to_edge_and_jump()
        self.place_plank_pillar()
        self.sneak_to_edge_and_jump()
        self.place_window_pillar()
        self.sneak_to_edge_and_jump()
        self.place_window_pillar()
        self.sneak_to_edge_and_jump()
        self.place_log_pillar()

        # Start wall right of the row of items
        self.move_camera(0, -90)
        self.sneak_to_edge_and_jump()

        # Place log pillar after entrance
        self.take_action('sneak forward', times=10) # Skip a block for entrance
        self.place_log_pillar()
        self.move_camera(-25, 180) # Turn around
        self.sneak_to_edge()
        self.take_action('sneak back', times=8)
        self.delay(10)
        self.take_action('place:planks') # Place roof above entrance
        self.delay(10)
        self.take_action('place:stone_slab')

        # Resume wall right of the row of items
        self.move_camera(25, 180) 
        self.sneak_to_edge()
        self.sneak_to_edge_and_jump()
        self.place_window_pillar()
        self.sneak_to_edge_and_jump()
        self.place_window_pillar()

        # Place wall behind the items
        self.move_camera(0, -90)
        self.sneak_to_edge_and_jump()
        self.place_window_pillar()
        self.sneak_to_edge_and_jump()
        self.place_window_pillar()
        self.sneak_to_edge_and_jump()
        self.place_plank_pillar()
        self.sneak_to_edge_and_jump()
        self.place_log_pillar()

        # Adjust angle to be able to place slabs at the agent's feet
        self.move_camera(-8, 0)
        self.take_action('sneak left', times=4) # Move to unfinished column on ceiling

        # Place ceiling slabs (3 x 3 grid)
        for i in range(3):
            self.take_action('sneak left', times=15)
            self.sneak_to_edge(backwards=True)
            for _ in range(3): # Place 3 slabs by moving backwards
                self.sneak_to_edge(backwards=True)
                self.take_action('sneak place:stone_slab')
            if i < 2: # Move to next column if not the last one
                self.take_action('sneak forward', times=60)
                self.sneak_to_edge()

        # Turn around
        self.move_camera(0, 180)
        self.sneak_to_edge()

        # Jump off roof
        self.sneak_to_edge()
        self.take_action('forward')
        self.notify_q.put(Message.SCRIPT_FINISHED)

    def place_log_pillar(self):
        """
        Place 3 logs followed by a slab
        """
        self.repeat(self.jump_and_place, 'log', times=3)
        self.place_slab()   

    def place_plank_pillar(self):
        """
        Place 3 planks followed by a slab
        """
        self.repeat(self.jump_and_place, 'planks', times=3)
        self.place_slab()

    def place_window_pillar(self):
        """
        Place a pillar with a window; glass in the middle with planks on top and bottom and a slab on top
        """
        self.jump_and_place('planks')
        self.jump_and_place('glass')
        self.jump_and_place('planks')
        self.place_slab()

    def jump_and_place(self, item):
        """
        Jump and place the specified item
        :param item: str, the item to place
        """
        self.take_action('jump')
        self.take_action('sneak place:' + item, times=5)
        self.delay(10)

    def sneak_to_edge(self, backwards=False):
        """
        Sneak to the edge of the block
        """
        direction = 'back' if backwards else 'forward'
        self.take_action(f'sneak {direction}', times=20)
    
    def sneak_to_edge_and_jump(self):
        """
        Sneak to the edge of the block and jump
        """
        self.sneak_to_edge()
        self.take_action('forward')
        self.delay(20)

    def place_slab(self):
        """
        Place a slab below the agent
        """
        self.take_action('jump')
        self.take_action('', times=3)
        self.take_action('place:stone_slab')
        self.delay(20)

    def nearby_smelt(self, item, delay=5):
        """
        Smelt the specified item using nearby furnace
        :param item: str, the item to smelt
        """
        self.take_action('nearbySmelt:' + item)
        self.delay(delay)

    def nearby_craft(self, item, delay=5):
        """
        Craft the specified item using nearby crafting table
        :param item: str, the item to craft
        """
        self.take_action('nearbyCraft:' + item)
        self.delay(delay)

    def craft_item(self, item, delay=5):
        """
        Craft the specified item
        :param item: str, the item to craft
        """
        self.take_action('craft:' + item)
        self.delay(delay)

    def repeat(self, func, param, times):
        """
        Repeat a function a specified number of times
        :param func: function, the function to repeat
        :param param: str, the parameter to pass to the function
        :param times: int, the number of times to repeat the function
        """
        for _ in range(times):
            func(param)

    def delay(self, ticks):
        """
        Delay the script for a specified number of seconds
        :param seconds: int, the number of seconds to delay
        """
        self.take_action('', times=ticks)