# Requirement 44

Files included:
- combat2.pth -- a model that successfully achieved a kill against a target
- fh_combat7.ipynb -- script used to train model

Link included:

https://drive.google.com/drive/folders/1HlwbYbP7knF20CZMNvWT14wGGNyAaVvr?usp=sharing

Link to drive hosted successful_kill.mp4 -- video of the successful kill. Video of the training session is 9 minutes and so exceeds the file size limit of GitHub, which is why it is hosted externally. The kill is achieved in the first 15 seconds of the video.

The provided video demonstrates that the new model is capable of defeating enemies under desirable conditions. The video includes a zombie that capable of attacking the agent but has restricted movement because of a partial fence between the zombie and the agent. The agent can be defeated by the zombie if either the agent or the zombie moves around the fence or the agent stays near the fence for an extended period of time, which occurs frequently during training. In the provided video, the agent uses the partial fence to attack the zombie while not approaching close enough to the fence to take lethal damage, and successfully kills the zombie.

The training environment makes a substantial difference in how effectively the agent is able to engage any enemy under limited training iterations. While the agent is not constrained within a limited area of movement, the agent does not attempt to fight and instead learns to away from the threat. This is both an easier sequence of inputs to learn and involves less risk of death. When the agent is constrained, it is much more likely to die but sometimes engages with the threat. This is dependent on how the agent is constrained and environmental factors in the area of movement. The agent overall performs poorly in regions only containing a perimeter wall or a hazardous perimeter wall, but performs better with barriers inside the area of movement. A potential cause for this discrepancy is that the fence provides a "safe" region for the agent where it can learn to attack the threat without as much risk of being attacked back. Without the fence, the agent is forced to move away from the threat constantly and face the threat to be able to attack it, which appears through repeated training to be a much more difficult skill to learn.
