<h1>Requirement 29</h1>
This requirement involved training an agent for iron collection. 
       
  
&nbsp;  
Successful completion of this task involved:
- Training the AI agent using with the provided MineRL environment MineRLObtainIronPickaxe-v0 using reinforcement learning and/or behavioral cloning, and uploading a short report with the results, including the number of times the agent successfully mines iron with each model
- This may optionally incorporate scripting/enhanced behavior, as to not repeat the training completed in previous requirements. This actually was not required, and the task was accomplished by Behavioral Cloning alone, which was impressive.
- Uploading the code for the best model. This can be found at: [Iron_BC_Train.ipynb](https://github.com/lincolnschick/ML4MC/blob/main/docs/reports/requirement-29/Iron_BC_Train.ipynb) 
- Uploading a video of the agent running trained with the best model and successfully mining iron.

  
<h2>Training</h2>
The MineRLObtainIronPickaxe-v0 dataset and environment were utilized for training. As in for Stone Collection, a NatureCNN was constructed for visual identification of the agent's surroundings. A batch size of 21 was used, since this quantity was determined to be optimal for stone collection, and it did not cause colab to crash. The learning rate and number of epochs were modified for experimentation. The optimal learning rate discovered was 0.0001. For epochs, models were trained for 2, 3, 4, and 5 epochs, with varieties of combinations of parameters. Each model took 3-5 hours to train. The training time for all of the models combined in this sprint was 20+ hours. 
<h2>Testing</h2>
Words 
    

Words

