import minerl
import gym
import numpy as np
from minerl.herobraine.env_specs.ml4mc_survival_specs import ML4MCSurvival
from ..scripts import mine_to_surface

# Digs down prior to testing the staircase_up function
def _dig_down():
    action_sequence = []
    action_sequence += [''] * 20  # Wait 1 sec
    action_sequence += ['camera:[9,0]'] * 6  # Look down 56 degrees
    
    # Loop to staircase down
    for _ in range(8):
      action_sequence += ['attack'] * 400 # Attack for 5 seconds to mine blocks
      action_sequence += ['forward'] * 20 # Walk forward for 1 second to move down the next level
    
    # Get random delta pitch and yaw (used to test ability to adjust camera)
    yaw = np.random.randint(-120, 120)
    pitch = np.random.randint(-120, 120)
    action_sequence += [f'camera:[{pitch},{yaw}]'] * 1 # Look in random direction

    # Get random ticks to move left (used to test moving to the center of a block)
    ticks = np.random.randint(1, 10)
    action_sequence += ['sneak left'] * ticks # Sneak left

    # Get random ticks to move right (used to test moving to the center of a block)
    ticks = np.random.randint(1, 10)
    action_sequence += ['sneak right'] * ticks # Sneak right
    return action_sequence

def _test():
    # Create the environment
    ml4mc_survival = ML4MCSurvival()
    ml4mc_survival.register() # Register with gym
    env = gym.make('ML4MCSurvival-v0')
    # env.make_interactive(port=5656)
    env.reset()

    # Dig down first
    for action in _dig_down():
        _ = mine_to_surface.take_action(env, action)

    # Test the script
    mine_to_surface.mine_to_surface(env)

if __name__ == "__main__":
    _test()