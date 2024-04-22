
<h1>Requirement 48</h1>
This requirement involved improving training an agent for surviving in a hostile environment.
       
  
&nbsp;  
Successful completion of this task involved:
- Training a new model for combat. The improved model: [improved_fight_enemies_model.pth](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-48/improved_fight_enemies_model.pth)
- Providing the code for training and testing. The testing and training are both included here: [final_combat.ipynb](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-48/final_combat.ipynb)
- A written report comparing this and the previous models: [readme.md](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-48/readme.md)
- Videos demonstrating the best model’s performance: [combat.mp4](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-48/combat.mp4)


<h2>Training and Testing</h2>
Similar to previous he survival environments, the agent was trained in a flat world, and the time was set to the middle of the night (18000 ticks). Mobs would appear frequently and approach the agent, creating hostile conditions. The key change made from previous iterations was setting the "always_attack" parameter to True. This allowed for the agent to more quickly acquire the aptitude to attack nearby enemies. Other changes in the environment layout and rewards system was also tested. 

<br/>
<br/>

In previous iterations, the agent only learned to occasionally punch the enemies, but in this iteration, it does so quite frequently. When in conditions similar to the training environment, with many mobs, the agent is able to defent itself and repel the enemies effectively. In peaceful conditions, the model often just punches nearbly objects, so it is implied that the model is to be invoked when the hostile environment is encountered in the interactor. It has been beneficial, in this sprint, to test the models immediately in the interactor, since we all have the full setup at this point. In a previous sprint, a model performed quite well in training, but the exact situation did not arise, so the intended behavior was not seen. However, we were able to make the adequate modifications in this sprint, since the interaction with the real world was able to be observed.
<br/>

Overall, the model has significantly improved since previous sprints, demonstrating a much stronger tendency to engage with enemies when they are present; it is significantly more focused on the goal of fighting and avoiding mobs. Therefore, the training was successful in accomplishing its goal. 

