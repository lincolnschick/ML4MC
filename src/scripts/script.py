from GUI.ml4mc_env import ML4MCEnv
from multiprocessing import Queue

SNEAK_SPEED = 0.065 # Blocks per tick

# Determine which axes to move on based on yaw
AXES_BY_YAW = { 0: 'xpos', 90: 'zpos', -90: 'zpos', 180: 'xpos', -180: 'xpos'}

# Determine which direction to move on the axes based on yaw
DIRECTIONS_BY_YAW = {
    0: {-1: 'right', 1: 'left'},
    90: {-1: 'right', 1: 'left'},
    -90: {-1: 'left', 1: 'right'},
    180: {-1: 'left', 1: 'right'},
    -180: {-1: 'left', 1: 'right'},
}

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

class Script:
    """
    Base class for all scripts
    :param ml4mc_env: ML4MCEnv, custom wrapper for MineRL environment
    :param notify_q: Queue, queue to send messages to the GUI when the script is finished
    """
    def __init__(self, ml4mc_env: ML4MCEnv, notify_q: Queue):
        self.ml4mc_env = ml4mc_env
        self.notify_q = notify_q

    def run(self):
        """
        Abstract method to run a script
        :return: None
        """
        raise NotImplementedError

    def take_action(self, action_str, times=1):
        """
        Takes an action (multiple times) and return final observation
        :param env: base MineRL environment
        :param action_str: string of action to take
        :param times: number of times to take the action
        :return: dict, final observation after taking the action
        """
        obs = None
        for _ in range(times):
            obs, _, _, _ = self.ml4mc_env.step(action_str)
        return obs

    def move_camera(self, pitch, yaw):
        """
        Moves the camera smoothly so the agent appears more human-like
        :param pitch: number of degrees to move the camera up or down
        :param yaw: number of degrees to move the camera left or right
        :return: dict, final observation after moving the camera
        """
        # Determine how many times to move the camera 10 degrees
        pitch_sign, yaw_sign = sign(pitch), sign(yaw)
        times = int(abs(pitch) // 10)
        obs = self.take_action(f'camera:[{10 * pitch_sign},0]', times)
        times = int(abs(yaw) // 10)
        obs = self.take_action(f'camera:[0,{10 * yaw_sign}]', times)

        # Move the remainder
        remainder = abs(pitch) % 10 * pitch_sign
        obs = self.take_action(f'camera:[{remainder},0]')
        remainder = abs(yaw) % 10 * yaw_sign
        obs = self.take_action(f'camera:[0,{remainder}]')
        return obs
    
    def center_agent_and_camera(self):
        """
        Centers the agent and camera on the block it is currently standing on
        :return: None
        """
        # Do a no-op to get starting observations
        obs = self.take_action('')
        
        # Determine how much to adjust the yaw to look directly at a block
        yaw = obs['location_stats']['yaw']
        closest_cardinal_yaw = round(yaw / 90) * 90

        # According to the documentation, the yaw should only be between -180 and 180.
        # However, experimentally, I found this is not always the case.
        if abs(closest_cardinal_yaw) > 180:
            closest_cardinal_yaw = (abs(closest_cardinal_yaw) - 180) * -sign(closest_cardinal_yaw)
        yaw_delta = closest_cardinal_yaw - yaw

        # Determine how much to adjust the pitch to look directly at a block
        pitch = obs['location_stats']['pitch']
        pitch_delta = 0 - pitch

        # Move the camera to be looking straight forward and alined with a cardinal direction
        obs = self.move_camera(pitch_delta, yaw_delta)

        yaw = closest_cardinal_yaw # Update the yaw to the new value
        pos = obs['location_stats'][AXES_BY_YAW[yaw]] # Get current position on the axis of interest
        delta = int(pos) + sign(pos) * 0.5 - pos # Record how far we are from the center of the block
        ticks = round(abs(delta) / SNEAK_SPEED) # Determine how many ticks to move
        if ticks > 0:
            obs = self.take_action(f'sneak {DIRECTIONS_BY_YAW[yaw][sign(delta)]}', ticks) # Move to the center of the block