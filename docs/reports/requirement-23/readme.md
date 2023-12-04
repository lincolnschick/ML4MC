<h1>Requirement 23</h1>
This requirement required training an agent for stone collection using Behavioral Cloning. BC was chosen rather than pure Reinforcement Learning to accelerate the learning process;
we were able to accomplish this with a significant degree of stochasitcity, allowing the agent to explore various solutions.

<h2>Training</h2>
For training, we utilized and modified the MineRLObtainIronPickaxe-v0 environment and datasets. A python script was written to modify the rewards system to promote stone collection,
along with discouraging looking up, since this was a common setback during training. The two primary hyperparameters that were tuned were epochs and batch size. The model
overfitted to the data at about 20 epochs, making this the estimated maximum threshold. The minimum threshold we discovered was five epochs, as this was often not enough training time
to fully understand the sequences of actions that attributed to a reward. The optimal number of epochs for our configuration was 15 epochs, since this allowed adequate
time to learn techniques and extrapolate to new situations. For batch size, a generally greater quanity allows for more efficient training; however, due to the limitations
for data usage in colab, the session would crash when a batch size greater than 30 was set. Therefore, we initialized the batch size to 21 to be safe. If we had access to
more computational resources, we could further improve our agent.
<h2>Testing</h2>
The model was tested using the custom environment we created in Requirement 26. The agent was initialized in a random seed, as to demonstrate that the model was not overfit to an
specific environment. The results are as follows:     
       
  
&nbsp;  
Episode #1 reward: 0.0   &emsp;&emsp;&nbsp;&nbsp;    episode length: 3000  
Episode #2 reward: 7.0   &emsp;&emsp;&nbsp;&nbsp;   episode length: 3000  
Episode #3 reward: 11.0  &emsp;&emsp; episode length: 3000  
Episode #4 reward: 0.0   &emsp;&emsp;&nbsp;&nbsp; episode length: 3000  
Episode #5 reward: 3.0   &emsp;&emsp;&nbsp;&nbsp;    episode length: 3000  
Episode #6 reward: 0.0 &emsp;&emsp;&nbsp;&nbsp; episode length: 1919  
Episode #7 reward: 12.0  &emsp;&emsp; episode length: 3000  
Episode #8 reward: 14.0  &emsp;&emsp; episode length: 3000  
Episode #9 reward: 0.0   &emsp;&emsp;&nbsp;&nbsp; episode length: 1444  
Episode #10 reward: 21.0 &emsp;&nbsp;&nbsp;  episode length: 3000  

The model was successful in obtaining stone in 6 out of the 10 episodes. The episodes where it was not successful can be attributed to both intrinsic and environmental factors. At times,
the agent would mine stone, but not collect it into its inventory. At other times, the agent would get stuck in a ravine or water; in one example, the agent attempted to mine stone
in the ocean. There is always room for improvement, but we were generally impressed with what the agent was able to accomplish given the constraints. When the agent was successful, 
it often continued this by mining the nearby stone blocks. It even displayed several advanced techniques, such as tunneling, as demonstrated by the video. It was overall a
fascinating process to observe the strategies it was able to learn. 
