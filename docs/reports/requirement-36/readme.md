<h1>Requirement 36</h1>
This requirement involved scripting and training an agent for diamond collection. Diamonds make up 0.016% of minerals in the game of Minecraft, so collecting one diamond in a run is an immense success.
       
  
&nbsp;  
Successful completion of this task involves:
- Training the AI agent using reinforcement learning and/or behavioral cloning, and uploading a short report with the results.
- Uploading the code for the best model
- Providing a script for diamond mining mimicking the strip mining approach that many players implement: [collect_diamonds.py](https://github.com/lincolnschick/ML4MC/blob/main/src/scripts/collect_diamonds.py)
- Uploading the results of running the script along with a video of the scripted agent obtaining diamonds: The script is above, and the videos are here: [finding_diamonds.mov](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-36/finding_diamonds.mov),  [staircase.mov](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-36/staircase.mov)
- Write a report comparing the two approaches: [readme.md](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-36/staircase.mov)

<h2>Scripting</h2>
The script was implemented by prompting the agent to staircase down to the level y=12, where it is statistically more probable to encounter a diamond. Once at this level, the agent 
mines forward until diamonds are discovered This may be a great distance, so the agent is given the capacity to switch to a new pickaxe. The pickaxe must be iron (or better) when it mines the diamonds, since this is a game mechanic, so this was ensured in the script.  The videos illustrated the ability for the agent to staircase to the correct level and dig from there 
as intended. The scripted agent was successful in encountering diamonds, which we were quite happy about. 

<h2>Testing</h2>
Referencing: [requirement36_diamondModelsData.pdf](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-36/requirement36_diamondModelsData.pdf)

Results for our first round of tests for diamond collect resulted in none of the generated models finding diamonds across 22 tests per each model (27 tests for the best performing model, four_epoch_diamond). Two of the models, two_epoch_diamond, and eight_epoch_diamond, were not effective, since they did not descend below the depth of 16. Diamonds can only be found between the depth range of 16 and 1, so this is a requirement. The model four_epoch_diamond was much more successful in this regard, descending below the depth of 16 in 7 out of 27 trials. Additionally, about 42.97% of this time was spent within the range of 5-12, which is the range where diamonds are more likely to occur. This is a nice positive start to diamond training.

<h2>Comparison</h2>
The diamond script significantly outperformed our initial series of tests for diamond collection, as the script was successful diamonds. Additionally, the scripted agent is able to always remain within the ideal y-level range of 5-12. Therefore, we will implement the diamond script in our UI, since it is reliable and effective in collecting diamonds. In the future, we may research more into BC diamond collection, since it is inherrently interesting and demonstrates a more organic approach. 
