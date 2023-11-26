import gym
import minerl
from minerl.herobraine.env_specs.stone_collection_specs import StoneCollection


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

def get_action_sequence():
    """
    Specify the action sequence for the agent to execute.
    """
    action_sequence = []
    action_sequence += [''] * 100  # Wait 5 sec

    action_sequence += ['camera:[9,0]'] * 6  # Look down 56 degrees
    
    # Loop to staircase down
    for _ in range(10):
      action_sequence += ['attack'] * 100 # Attack for 5 seconds to mine blocks
      action_sequence += ['forward'] * 20 # Walk forward for 1 second to move down the next level
    
    action_sequence += ['camera:[0,20]'] * 9 # Turn around 180 degrees

    # Loop to return to above ground
    for _ in range(10):
        action_sequence += ['forward'] * 15 # Move to end of current stair
        action_sequence += ['jump'] 
        action_sequence += ['forward'] * 15 # Move onto next stair

    action_sequence += ['camera:[-9,0]'] * 6 # Restore camera view
    action_sequence += ['attack'] * 30 # Break block at end of staircase to get out (not always necessary)

    # Jump to get out
    action_sequence += ['forward'] * 15
    action_sequence += ['jump']
    action_sequence += ['forward'] * 15
    return action_sequence


def main():
    abs_STONE = StoneCollection()
    abs_STONE.register() # Register with gym
    env = gym.make('StoneCollection-v0')
    # env.make_interactive(port=5656)
    action_sequence = get_action_sequence()

    env.reset()

    total_reward = 0
    for i, action in enumerate(action_sequence):
        obs, reward, done, _ = env.step(str_to_act(env, action))
        env.render()
        total_reward += reward
        if done:
            break

    print(f'\nTotal reward = {total_reward}')

if __name__ == "__main__":
    main()