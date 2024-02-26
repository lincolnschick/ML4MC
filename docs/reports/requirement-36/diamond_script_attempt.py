import minerl
import gym


SNEAK_SPEED = 0.065 # Blocks per tick

# Determine which axes to move on based on yaw
AXES_BY_YAW = { 0: 'x', 90: 'z', -90: 'z', 180: 'x', -180: 'x'}

# Determine which direction to move on the axes based on yaw
DIRECTIONS_BY_YAW = {
    0: {-1: 'right', 1: 'left'},
    90: {-1: 'right', 1: 'left'},
    -90: {-1: 'left', 1: 'right'},
    180: {-1: 'left', 1: 'right'},
    -180: {-1: 'left', 1: 'right'},
}

# Amount of time we should mine for each pickaxe type
# Padded based on tests to account for lag and mining dirt/sand at surface
MINING_SECS_BY_PICKAXE = {
    'iron_pickaxe': 1.0,
    'stone_pickaxe': 1.2,
    'wooden_pickaxe': 1.45,
}

def str_to_act(env, actions):
    """
    Simplifies specifying actions for the scripted part of the agent.
    Some examples for a string with a single action:
        'craft:planks'
        'camera:[10,0]'
        'attack'
        'jump'
        ''
    There should be no spaces in single actions, as we use spaces to separate actions with multiple "buttons" pressed:
        'attack sprint forward'
        'forward camera:[0,10]'

    :param env: base MineRL environment.
    :param actions: string of actions.
    :return: dict action, compatible with the base MineRL environment.
    """
    act = env.action_space.noop()
    for action in actions.split():
        if ":" in action:
            k, v = action.split(':')
            if k == 'camera':
                act[k] = eval(v)
            else:
                act[k] = v
        else:
            act[action] = 1
    return act

def secs_to_ticks(seconds):
    """
    Convert seconds to ticks; there are 20 ticks per second in Minecraft
    :param seconds: number of seconds to convert
    :return: int, number of ticks
    """
    return int(seconds * 20)

def sign(num):
    """
    Convert a number into its sign
    :param num: number to convert
    :return: int, sign of the number: -1 or 1
    """
    return 1 if num >= 0 else -1

def take_action(env, action_str, times=1):
    """
    Takes an action (multiple times) and return final observation
    :param env: base MineRL environment
    :param action_str: string of action to take
    :param times: number of times to take the action
    :return: dict, final observation after taking the action
    """
    obs = None
    for _ in range(times):
        obs, _, _, _ = env.step(str_to_act(env, action_str))
        env.render()
    return obs

def move_camera(env, pitch, yaw):
    """
    Moves the camera smoothly so the agent appears more human-like
    :param env: base MineRL environment
    :param pitch: number of degrees to move the camera up or down
    :param yaw: number of degrees to move the camera left or right
    :return: dict, final observation after moving the camera
    """
    # Determine how many times to move the camera 10 degrees
    pitch_sign, yaw_sign = sign(pitch), sign(yaw)
    times = int(abs(pitch) // 10)
    obs = take_action(env, f'camera:[{10 * pitch_sign},0]', times)
    times = int(abs(yaw) // 10)
    obs = take_action(env, f'camera:[0,{10 * yaw_sign}]', times)

    # Move the remainder
    remainder = abs(pitch) % 10 * pitch_sign
    obs = take_action(env, f'camera:[{remainder},0]')
    remainder = abs(yaw) % 10 * yaw_sign
    obs = take_action(env, f'camera:[0,{remainder}]')
    return obs

def equip_best_pickaxe(env, obs):
    """
    Equips the most efficient pickaxe we have and return the observation and time to mine a block based on this
    :param env: base MineRL environment
    :param obs: dict, current observation
    :return: dict, observation after equipping the best pickaxe, name of the pickaxe, and time to mine a block
    """
    inventory = obs['inventory']
    for pickaxe, secs in MINING_SECS_BY_PICKAXE.items():
        if pickaxe in inventory and inventory[pickaxe] > 0:
            obs = take_action(env, f'equip:{pickaxe}')
            return obs, pickaxe, secs_to_ticks(secs)
    
    # We have no pickaxes, so return default values for bare hand
    return obs, None, secs_to_ticks(8)

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

def check_broken_pickaxe_or_stuck(prev_inventory, handled_iron_bug, pickaxe, env):
    cur_pos = (obs['location_stats']['xpos'], obs['location_stats']['zpos'])
    # Check if pickaxe has broken
    if pickaxe and obs['equipped_items']['mainhand']['type'] != pickaxe:
        # Equip best pickaxe we have and update time to mine a block
        obs, pickaxe, mine_ticks = equip_best_pickaxe(env, obs)
    elif prev_pos == cur_pos: # Check if we are stuck (and we know its not because our pickaxe broke)
        mine_ticks *= 2 # Double time to mine a block (could be facing ore, wood, etc.)
    prev_pos = cur_pos

    # Correction for iron pickaxe bug
    if pickaxe == 'iron_pickaxe' and not handled_iron_bug and is_mining_dirt(prev_inventory, obs):
        mine_ticks += 6 # Increase time to mine a block
        handled_iron_bug = True

    # Update previous inventory
    prev_inventory = obs['inventory']

def get_on_y12(env, obs, mine_ticks, prev_inventory, handled_iron_bug, pickaxe):
    check_broken_pickaxe_or_stuck(prev_inventory, handled_iron_bug, pickaxe, env)
    while(obs['location_stats']['y'] > 12):
        # Look down 56 degrees 
        obs = move_camera(env, -56, 0)
        obs = take_action(env, 'attack', mine_ticks)
        action_sequence += ['forward'] * 20 # Walk forward for 1 second to move down the next level
        
    while(obs['location_stats']['y'] < 12):
        check_broken_pickaxe_or_stuck(prev_inventory, handled_iron_bug, pickaxe, env)

        # Look straight up 
        obs = move_camera(env, -90, 0)
         # Mine block above agent
        obs = take_action(env, 'attack', mine_ticks)

        # Look at next block (pitch becomes -60)
        obs = move_camera(env, 30, 0)

        # Mine next block
        obs = take_action(env, 'attack', mine_ticks)

        # Look straight at final block (pitch becomes 0)
        obs = move_camera(env, 60, 0)

        # Mine final block
        obs = take_action(env, 'attack', mine_ticks)

        # Jump and move forward to move onto next stair level
        obs = take_action(env, 'jump')
        obs = take_action(env, 'sprint forward', secs_to_ticks(0.75))
        

# def has_not_found_diamonds(prev_inventory, obs, pickaxe):


def mine_for_diamonds(env: gym.Env) -> None:
    """
    Has the agent dig to y=12 and mine for diamonds at this level
    :return: None
    """

    # Do a no-op to get starting observations
    obs = take_action(env, '')

    # Determine how much to adjust the yaw to look directly at a block
    yaw = obs['location_stats']['yaw']
    closest_cardinal_yaw = round(yaw / 90) * 90
    yaw_delta = closest_cardinal_yaw - yaw

    # Determine how much to adjust the pitch to look directly at a block
    pitch = obs['location_stats']['pitch']
    pitch_delta = 0 - pitch

    # Move the camera to be looking straight forward and alined with a cardinal direction
    obs = move_camera(env, pitch_delta, yaw_delta)

    yaw = int(obs['location_stats']['yaw']) # Get current yaw, needed to determine which direction to move
    prev_pos = obs['location_stats'][f'{AXES_BY_YAW[yaw]}pos'] # Get current position on the axis of interest
    delta = int(prev_pos) + sign(prev_pos) * 0.5 - prev_pos # Record how far we are from the center of the block
    ticks = round(abs(delta) / SNEAK_SPEED) # Determine how many ticks to move
    if ticks > 0:
        obs = take_action(env, f'sneak {DIRECTIONS_BY_YAW[yaw][sign(delta)]}', ticks) # Move to the center of the block

    
    # Equip best pickaxe we have and set time to mine a block    
    obs, pickaxe, mine_ticks = equip_best_pickaxe(env, obs)

    # Set up variables for loop
    prev_inventory = None
    prev_pos = None
    handled_iron_bug = False

    # Get on the ideal y-level for finding diamonds
    get_on_y12(env, obs, mine_ticks, prev_inventory, handled_iron_bug, pickaxe)
    obs = move_camera(env, 10, 0) # Look down 10 degrees so we mine the two blocks in front of the agent

    # Loop to mine for diamonds
    while 'diamond' in obs['inventory'] and obs['inventory']['diamond'] < 0:
        check_broken_pickaxe_or_stuck(prev_inventory, handled_iron_bug, pickaxe, env)
        obs = take_action(env, 'sprint forward', secs_to_ticks(0.75))
        obs = take_action(env, 'attack', mine_ticks*2) # Mine the upper and lower blocks
        get_on_y12(env, obs, mine_ticks, prev_inventory, handled_iron_bug, pickaxe) # Return to y=12 if the agent has changed levels