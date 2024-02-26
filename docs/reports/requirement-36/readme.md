<h1>Requirement 36</h1>
This requirement involved scripting and training an agent for diamond collection. Diamonds make up 0.016% of minerals in the game of Minecraft, so collecting one diamond in a run is an immense success.
       
  
&nbsp;  
Successful completion of this task involves:
- Training the AI agent using reinforcement learning and/or behavioral cloning, and uploading a short report with the results.
- Uploading the code for the best model
- Providing a script for diamond mining mimicking the strip mining approach that many players implement: [collect_diamonds.py](https://github.com/lincolnschick/ML4MC/blob/main/src/scripts/collect_diamonds.py)
- Uploading the results of running the script along with a video of the scripted agent obtaining diamonds: The script is above, and the videos are here: [finding_diamonds.mov](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-36/finding_diamonds.mov),  [staircase.mov](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-36/staircase.mov)
- Write a report comparing the two approaches: [readme.md](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-36/staircase.mov)

  
<h2>Training</h2>

<h2>Scripting</h2>
The script was implemented by prompting the agent to staircase down to the level y=12, where it is statistically more probable to encounter a diamond. Once at this level, the agent 
mines forward until diamonds are discovered This may be a great distance, so the agent is given the capacity to switch to a new pickaxe. The pickaxe must be iron (or better) when it mines the diamonds, since this is a game mechanic, so this was ensured in the script.  The videos illustrated the ability for the agent to staircase to the correct level and dig from there 
as intended. The scripted agent was successful in encountering diamonds, which we were quite happy about. 

<h2>Testing</h2>
Results for our first round of tests for diamond collect resulted in none of the three generated models finding diamonds across 22 tests per each model (27 tests for the best performing model, four_epoch_diamond). Two of the models, two_epoch_diamond, and eight_epoch_diamond, showed very negative results, often dying early with each test. Neither of these two models were able to descend below the depth of 16. This depth is important because diamonds can only be found between the depth range of 16 and 1. four_epoch_diamond was much more successful in this regard, descending below the depth of 16 in 7 out of 27 trials. Additionally, about 42.97% of this time was spent within the range of 5-12, which is the range where diamonds are more likely to occur. This is a nice positive start to diamond training.

<h2>Comparison</h2>
Clearly the script for diamond collection was able to do a lot better than our initial series of tests for diamond collection, as the script was actually able to find diamonds. Additionally, the scripted agent is able to always stay within the 5-12 range instead of wandering to other depths. However, in their current states, both methods have a high likelihood of dying if they encounter hostile environments such as monsters and lava, as neither are equipped to deal with these issues. 
