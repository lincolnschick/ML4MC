
<h1>Requirement 38</h1>
This requirement involved training an agent for surviving in a hostile environment.
       
  
&nbsp;  
Successful completion of this task involved:
- Creating an environment with hostile conditions, which can be observed in the video below
- Utilizing a model that rewards for the amount of time the agent spends in the game
- Providing the code for training and testing
- A written report describing the best model
- Videos demonstrating the best model’s performance

       - [](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-29/SuccessfulIronCollectionVideo.mp4)

  
<h2>Training and Testing</h2>
In order to train the AI on the task of combatting mobs in Minecraft, the environment reward handlers for the AI agent had to be modified to allow for the script to detect new features of the agent’s environment. For this sprint, we decided to test out new handlers for when the agent took damage, and for when the agent gained XP upon defeating an enemy mob. These additions were added to reward.py within the code of MineRL, and are labeled RewardForTakingDamage(), and RewardForXPGain() respectively.


