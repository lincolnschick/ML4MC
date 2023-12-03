<h1>Requirement 23</h1>
This requirement required training an agent for stone collection using Behavioral Cloning. 

<h2>Training</h2>
For training, we utilized and modified the MineRLObtainIronPickaxe-v0 environment and datasets. A python script was written to modify the rewards system to promote stone collection,
along with discouraging looking up, since this was a common setback during training. The two primary hyperparameters that were tuned were epochs and batch size.
<h2>Testing</h2>
The model was tested using the custom environment we created in Requirement 26. The agent was initialized in a random seed, as to demonstrate the agent was not overfit to an
optimal environment. The results are as follows:     
       
  
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
in the ocean. There is always room for improvement, but we were overall impressed with what the agent was able to accomplish given the constraints. When the agent was successful, 
it often continued this by mining the nearby stone blocks. It even displayed several advanced techniques, such as tunneling, as demonstrated by the video. It was overall a
fascinating process to observe the strategies it was able to learn. 
