<h1>Requirement 29</h1>
This requirement involved training an agent for iron collection. 
       
  
&nbsp;  
Successful completion of this task involved:
- Training the AI agent using with the provided MineRL environment MineRLObtainIronPickaxe-v0 using reinforcement learning and/or behavioral cloning, and uploading a short report with the results, including the number of times the agent successfully mines iron with each model
       - [2EpochsIron.pth](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-29/2EpochIron.pth) : one successful test case, 4 iron_ore mined
       - [3EpochsIron.pth](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-29/3EpochIron.pth) : one successful test case, 2 iron_ore mined
- This may optionally incorporate scripting/enhanced behavior, as to not repeat the training completed in previous requirements. This actually was not required, and the task was accomplished by Behavioral Cloning alone, which was impressive.
- Uploading the code for the best model. This can be found at: [Iron_BC_Train.ipynb](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-29/Iron_BC_Train.ipynb) 
- Uploading a video of the agent running trained with the best model and successfully mining iron:
       - [SuccessfulIronRewardsScreenshot.png](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-29/SuccessfulIronRewardsScreenshot.png)
       - [SuccessfulIronCollectionVideo.mp4](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-29/SuccessfulIronCollectionVideo.mp4)

  
<h2>Training</h2>
The MineRLObtainIronPickaxe-v0 dataset and environment were utilized for training. As in for Stone Collection, a NatureCNN was constructed for visual identification of the agent's surroundings. A batch size of 21 was used, since this quantity was determined to be optimal for stone collection, and it did not cause colab to crash. The learning rate and number of epochs were modified for experimentation. The optimal learning rate discovered was 0.0001. For epochs, models were trained for 2, 3, 4, and 5 epochs, with varieties of combinations of parameters. Each model took 3-5 hours to train. The training time for all of the models combined in this sprint was 20+ hours. 
<h2>Testing</h2>
For testing purposes, the models were run through a modified training environment that starts the agent in the "extreme_hills" biome with a pickaxe. This was done with the intent of speeding up the rate at which the agent collects iron in any given test instance. Agents were set to navigate the environment for a total of 40000 steps of the environment, translating to approximately 10 minutes of gameplay video footage. Tests were terminated early in the event of the agent's death.

Eight models were compared in the testing environment. Two of them proved superior, namely 2EpochsIron.pth and 3EpochsIron.pth. The models with more epochs trained did not match this performance, likely due to overfitting. The metrics for each of the two can be found at [SuccessfulIronRewardsScreenshot.png](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-29/SuccessfulIronRewardsScreenshot.png).  Iron is a very scarce resource in Minecraft, meaning that we'll expect to see fewer passing tests for this task than for previous tasks, so this level of collection is expected for the amount of time provided during training. Furthermore, all model's displayed "humanlike" behavior imitating how a human minecraft player would go about mining iron, by digging downward, and fanning out underground; it was fascinating to see the strategies they developed.

