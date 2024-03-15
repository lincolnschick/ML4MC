from scripts.script import Script, secs_to_ticks

DESCENT_TICKS_BY_PICKAXE = {
    'iron_pickaxe': 60,
    'stone_pickaxe': 60,
    'wooden_pickaxe': 87,
}

STRIP_TICKS_BY_PICKAXE = {
    'iron_pickaxe': 30,
    'stone_pickaxe': 40,
    'wooden_pickaxe': 58,
}

class GatherStoneScript(Script):
    def __init__(self, ml4mc_env, notify_q):
        super().__init__(ml4mc_env, notify_q)
        self.mining_ticks = None

    def equip_pickaxe(self, obs, descent=True):
        """
        Equips the most efficient pickaxe we have and return the observation and time to mine a block based on this
        :param obs: dict, current observation
        :return: dict, observation after equipping the best pickaxe and time to mine a block
        """
        print('Equipping pickaxe')
        inventory = obs['inventory']
        ticks_dict = DESCENT_TICKS_BY_PICKAXE if descent else STRIP_TICKS_BY_PICKAXE
        for pickaxe, ticks in ticks_dict.items():
            if pickaxe in inventory and inventory[pickaxe] > 0:
                obs = self.take_action(f'equip:{pickaxe}')
                self.mining_ticks = ticks
                return obs
        
        # We have no pickaxes, so set default value for bare hand
        self.mining_ticks = 160
        return obs
    
    def mine_to_depth(self):
        """
        Mines to down 10 blocks from surface
        :return: None
        """
        self.center_agent_and_camera()

        # Look down 60 degrees and equip pickaxe to prepare for loop
        obs = self.move_camera(60, 0)
        obs = self.equip_pickaxe(obs) # Equip best pickaxe
        
        # Get current y-level to determine how far we need to mine
        y = int(obs['location_stats']['ypos'])

        dest_y = y - 10
        # Mine down 10 blocks
        while y > dest_y:
            if obs['equipped_items']['mainhand']['type'] not in DESCENT_TICKS_BY_PICKAXE: # Equip new pickaxe if it breaks
                obs = self.equip_pickaxe(obs)
            obs = self.take_action('attack', self.mining_ticks) # Mine 3 blocks below agent
            obs = self.take_action('sprint forward', secs_to_ticks(0.75)) # Move forward to mine next block
            y = int(obs['location_stats']['ypos']) # Update Y-level

    def run(self):
        """
        Collects diamonds by mining to Y-level 12 and then strip mining.
        Assumes the agent is currently above Y-level 12 and has sufficient iron pickaxes.
        :return: None
        """
        self.mine_to_depth()
        # Look 30 degrees below horizon to prepare for loop (started from 60 degrees in mine_to_depth)
        obs = self.move_camera(-30, 0)

        # Update pickaxe for strip mining
        obs = self.equip_pickaxe(obs, descent=False) 
        while True:
            if obs['equipped_items']['mainhand']['type'] not in STRIP_TICKS_BY_PICKAXE: # Equip new pickaxe if it breaks
                obs = self.equip_pickaxe(obs, descent=False)
            obs = self.take_action('attack', self.mining_ticks)
            self.take_action('sprint forward', secs_to_ticks(0.5))