# Requirement 26
## Results
From the requirement artifact: "*Completion of this task will be shown by uploading the code for the created environment to our github and showing a video of an AI agent exploring our custom environment, and receiving a reward for collecting stone.*"

- The code for the custom environment requirement can be found at [stone_collection_specs.py](https://github.com/lincolnschick/minerl/blob/955dc359165e1348ffe1404b2c81b2bfd6a45241/minerl/herobraine/env_specs/stone_collection_specs.py).
- The video of the AI agent exploring the environment and its corresponding reward can be found at [stoneCollection_demo.mp4](https://github.com/lincolnschick/ML4MC/blob/custom_env/src/custom_envs/stoneCollection/stoneCollection_demo.mp4).
    - The code for the tests can be found at [stoneCollection_solution.py](https://github.com/lincolnschick/ML4MC/blob/custom_env/src/custom_envs/stoneCollection/stoneCollection_solution.py).

## Findings
### Discouraging Certain Behaviors
We discussed discouraging digging straight down, and avoiding water and lava; however, I found that although you can set negative rewards for certain actions, there is currently no support on the Python side for detecting coming into contact with water or lava nor using coordinates to detect digging straight down. There may be support on the Malmo/Java side though, so this is something we could implement in the future.

RewardHandlers are currently limited to:
- ConstantReward
- RewardForCollectingItems
- RewardForCollectingItemsOnce
- RewardForMissionEnd
- RewardForTouchingBlockType
- RewardForDistanceTraveledToCompassTarget

### Recording Colab Videos with Editable Minerl
For some reason I was unable to debug, when minerl is installed from Google Drive, colabgymrender.recorder.Recorder initialization throws a permission error. I tried it without any of my changes (directly from GitHub), and it was still an issue. We may just have to record locally if we can't fix it.

### Using Custom Environments in Behavioral Cloning Training
We also wanted to explore whether it is possible to use the custom environments' reward functions during behavioral cloning training by using a dataset created with a different environment. While it turned out to be possible to suppress enough errors to make this happen through adding our environment's name to a dictionary in MineRL and renaming the dataset, it is useless because the reward is part of the dataset. Thus, the custom environments will likely just be used for reinforcement learning.
<img width="1154" alt="datasetrewards" src="https://github.com/lincolnschick/ML4MC/assets/68517913/97f61648-d629-4128-9659-00204a9f91b1">
