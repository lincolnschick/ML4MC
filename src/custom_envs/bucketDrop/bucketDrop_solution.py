"""Solution code for the mlg_wb gym"""
# Slightly modified to reflect our naming scheme and slow visual output

__author__ = "Sander Schulhoff"
__email__ = "sanderschulhoff@gmail.com"

# initialization steps
from time import sleep
import gym
from bucketDrop_source import BUCKETDROP

SLEEP_TIME = 0.1

# In order to use the environment as a gym you need to register it with gym
abs_BUCKET = BUCKETDROP()
abs_BUCKET.register()
env = gym.make("BucketDrop-v0")
obs  = env.reset()

# move back and look down
for i in range(21):
    action = env.action_space.noop()
    action["back"] = 1
    obs, reward, done, info = env.step(action)
    env.render()
    sleep(SLEEP_TIME)
    
for i in range(20):
    action = env.action_space.noop()
    action["back"] = 0
    action["camera"] = [5, 0]
    obs, reward, done, info = env.step(action)
    env.render()
    sleep(SLEEP_TIME)

while obs["location_stats"]["ypos"] > 7.5:
    action = env.action_space.noop()
    obs, reward, done, info = env.step(action)
    env.render()
    sleep(SLEEP_TIME)

# place the water bucket
action = env.action_space.noop()
action["use"] = 1
obs, reward, done, info = env.step(action)
env.render()
sleep(SLEEP_TIME)

# noop
action = env.action_space.noop()
print(action, obs["life_stats"])
obs, reward, done, info = env.step(action)
env.render()
sleep(SLEEP_TIME)

# pick the water back up
action = env.action_space.noop()
action["use"] = 1
obs, reward, done, info = env.step(action)
env.render()
sleep(SLEEP_TIME)

# equip the pickaxe
action = env.action_space.noop()
action["equip"] = "diamond_pickaxe"
obs, reward, done, info = env.step(action)
env.render()
sleep(SLEEP_TIME)

# mine the gold block
while not done:
    action = env.action_space.noop()
    action["attack"] = 1
    obs, reward, done, info = env.step(action)
    env.render()
    sleep(SLEEP_TIME)