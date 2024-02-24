<h1>Requirement 36</h1>
This requirement involved scripting and training an agent for diamond collection. Diamonds make up 0.016% of minerals in the game of Minecraft, so collecting one diamond in a run is an immense success.
       
  
&nbsp;  
Successful completion of this task involves:
- Training the AI agent using reinforcement learning and/or behavioral cloning, and uploading a short report with the results.
- Uploading the code for the best model
- Providing a script for diamond mining mimicking the strip mining approach that many players implement: [collect_diamonds.py](https://github.com/lincolnschick/ML4MC/blob/main/src/scripts/collect_diamonds.py)
- Uploading the results of running the script along with a video of the scripted agent obtaining diamonds (if it finds any): The script is above, and the videos are here: [finding_diamonds.mov](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-36/finding_diamonds.mov),  [staircase.mov](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-36/staircase.mov)
- Write a report comparing the two approaches: [readme.md](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-36/staircase.mov)

  
<h2>Training</h2>

<h2>Scripting</h2>
The script was implemented by prompting the agent to staircase down to the level y=12, where it is statistically more probable to encounter a diamond. Once at this level, the agent 
mines forward until diamonds are discovered This may be a great distance, so the agent is given the capacity to switch to a new pickaxe. The pickaxe must be iron (or better) when it mines the diamonds, since this is a game mechanic, so this was ensured in the script.  The videos illustrated the ability for the agent to staircase to the correct level and dig from there 
as intended. The scripted agent was successful in encountering diamonds, which we were quite happy about. 

<h2>Comparison</h2>
