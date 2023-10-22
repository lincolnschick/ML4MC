import gym
import cv2
import minerl
from minerl.data import BufferedBatchIter
from treeChop_optimized import TreeOpt
import pprint

abs_TO = TreeOpt()
abs_TO.register()

def render(observation):
    inventory = observation["inventory"]
    # Clean up inventory info a bit: if no item in inventory, remove its print
    for key in list(inventory.keys()):
        if inventory[key] == 0:
            _ = inventory.pop(key)
        else:
            # Remove numpy array and just replace with int
            inventory[key] = inventory[key].item()
    print("Inventory:\n", pprint.pformat(inventory, indent=4, width=10))
    # Make it larger for easier reading
    image = observation["pov"]
    image = cv2.resize(image, (256, 256))
    cv2.imshow("minerl-image", image[..., ::-1])
    # Refresh image
    _ = cv2.waitKey(1)

def main():
    env = gym.make("MineRLTreeOpt-v0")
    obs = env.reset()

    done = False
    while(not done):
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
        render(obs)
    env.close()

if __name__ == "__main__":
    main()