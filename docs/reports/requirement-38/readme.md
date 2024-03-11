
<h1>Requirement 38</h1>
This requirement involved training an agent for surviving in a hostile environment.
       
  
&nbsp;  
Successful completion of this task involved:
- Creating an environment with hostile conditions, which can be observed in the video below
- Utilizing a model that rewards for the amount of time the agent spends in the game: [combat.pth](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-38/combat.pth)
- Providing the code for training and testing. The testing and trainin are both included here: [fh_combat_test.ipynb](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-38/fh_combat_test.ipynb)
- A written report describing the best model: [readme.md](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-38/readme.md)
- Videos demonstrating the best model’s performance: [avoid_mobs](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-38/avoid_mobs.mp4)

<h2>Training and Testing</h2>
In order to train the AI on the task of combatting mobs in Minecraft, the environment reward handlers for the AI agent had to be modified to allow for the script to detect new features of the agent’s environment. For this sprint, we decided to test out new handlers for when the agent took damage, and for when the agent gained XP upon defeating an enemy mob. These additions were added to reward.py within the code of MineRL, and are labeled RewardForTakingDamage(), and RewardForXPGain() respectively.


\n
Upon implementation, it was clear that the agent had a great capacity for avoiding taking damage. It would run as quickly as it could, hitting enemy entities out of the way. This is quite valuable for survival, so it is successful in this regard. However, we would prefer if the enemies were eliminated from the map entirely. Because it was optimized for the task of avoiding xp reduction, it often did not get the chance to fully attack the enemies to gain XP. Hence, another iteration is desired. Further, 15+ hours were spent in the attempt to create a smaller survival arena where the agent could fight a mob in a constrained manner. It would take 20+ min to run each attempt. We were successful in creating the box, but the agent was frozen for the duration of the test; the reason for this is yet to be discovered. Differing layouts and initial positions of the agent were tested, but none successful. Moving forward, there will likely be a greater emphasis on XP rewards and perhaps a new environment if this configuration is able to be created. 

Therefore, our agent has acquired a technique for surviving in hostile conditions; further iterations will be completed to thoroughly remove the harmful entities. 

