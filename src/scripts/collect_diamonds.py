from scripts.script import Script, secs_to_ticks
from GUI.ml4mc_env import ML4MCEnv


class CollectDiamondsScript(Script):
    def __init__(self, ml4mc_env: ML4MCEnv):
        super().__init__(ml4mc_env)
    
    def mine_to_depth(self):
        """
        Mines to Y-level 12
        :return: None
        """
        self.center_agent_and_camera()

        # Look down 60 degrees and equip pickaxe to prepare for loop
        obs = self.move_camera(60, 0)
        obs = self.take_action(f'equip:iron_pickaxe')
        
        # Get current y-level to determine how far we need to mine
        y = int(obs['location_stats']['ypos'])
        mining_ticks = secs_to_ticks(3) # Time to mine down 3 blocks with iron pickaxe

        # Mine to Y-level 12
        while y > 12:
            obs = self.take_action('attack', mining_ticks) # Mine blocks below agent
            obs = self.take_action('forward', secs_to_ticks(0.75)) # Move forward to mine next block
            y = int(obs['location_stats']['ypos']) # Update Y-level

    def run(self):
        """
        Collects diamonds by mining to Y-level 12 and then strip mining.
        Assumes the agent is currently above Y-level 12 and has sufficient iron pickaxes.
        :return: None
        """
        self.mine_to_depth()

        # Look 40 degrees below horizon to prepare for loop (started from 60 degrees in mine_to_depth)
        self.move_camera(-20, 0)
        mining_ticks = secs_to_ticks(1.75) # Time to mine 2 blocks with iron pickaxe
        while True:
            self.take_action('attack', mining_ticks)
            self.take_action('forward', secs_to_ticks(0.5))