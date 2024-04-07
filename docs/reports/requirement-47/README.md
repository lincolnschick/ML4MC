# Requirement 47 - Perform second attempt at training for diamond collection
From the artifact:
Successful completion of this requirement includes:
- Training the AI agent using reinforcement learning and/or behavioral cloning, and uploading a short report with the results.
- Uploading code for the best model.
- Write a report comparing the model's performance to the previous iteration of this requirement, and detailing how this approach was different.

### RL
The first attempt at training for diamond collection was centered around behavioral cloning. This sprint, one of our approaches was to use reinforcement learning. At first, we tried simply training using the rewards we already had, e.g., rewards for collecting dirt, cobblestone, and diamonds, and hoping the agent would learn to dig down and find diamonds that way, but we quickly realized this would not be sufficient. Training was ineffective as the agent was not digging down. Two breakthroughs helped us overcome this barrier. 

First, we realized we could modify the Java code in Malmo for RewardForDistanceTraveledToCompassTarget by letting the target be the current X and Z coordinates at Y=12. This would reward the agent for digging down towards Y=12 and punish the agent for digging up above Y=12 or below it. 

The second breakthrough involved realizing that the always_attack parameter on the model ActionShaping was set to False. Setting this to True meant that the model would always complete an attack action every tick.

Both these changes caused the agent to promptly dig down during training, which was good.

Unfortunately, all the models trained were unable to stop digging down at Y=12. In hindsight, this is likely because although our reward functions have access to the agent's current height, the models do not. They only use the POV of the agent. There are no visual cues indicating how deep the agent is, and each spawn is at a slighlty different height, so one never knows how far to dig down. Thus, no models were able to collect any diamonds as they usually got stuck at bedrock if they survived that long.

- The best model is [here](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-47/RL/diamond_rl_best_model.pth).
- The Colab for training is [here](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-47/RL/Diamond_RL.ipynb).
- Videos of training and testing are [here](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-47/RL/rl_training_footage.mp4) and [here](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-47/RL/rl_test_footage.mov).

### RL With Pretraining
One idea we had was to train a model first using our diamond dataset and follow it up with reinforcement learning. This was a solution to the initial difficulty we had getting our agents to begin digging down with pure RL.

Our training infrastructure is built using stablebaselines3, so naturally, when we came across some documentation for pretraining with stablebaselines (earlier version), this seemed like the obvious choice. However, stablebaslines requires Python 3.7 and many outdated dependencies. We attempted to install Python 3.7 on Colab and fix the dependencies, but Google Colab makes this process very difficult, and we were unsuccessful. 