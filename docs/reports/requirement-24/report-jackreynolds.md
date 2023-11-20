# Imitation Learning in BASALT (Benchmark for Agents that Solve Almost-Lifelike Task) Environments

### Contents

* Introduction
* Methods and Procedure
* Results
* Discussion

### Introduction

For this requirement, our objective was to train our model using Imitation Learning on the FindCave environment.
I opted to implement a *genetic algorithm* for the BASALT FindCave with the hopes of improving performance from the previous sprint.
This algorithm can also be run with several devices in parallel using a shared Google Drive folder.

### Methods and Procedure

The included *OptimizerBASALT.ipynb* notebook file can be used to implement a genetic algorithm in Google Colab + Drive.

The setup steps are:
* Create a folder to share across multiple Google accounts in Google Drive
* Create a samples.csv file to store hyperparameters of epochs, learning rate, and batch size that you want to explore
* Update the path in the *OptimizerBASALT.ipynb* to the shared Drive path

After setting a workspace through these steps, the genetic algorithm can be run on multiple computers simultaneously.
Simply open the file on different Google accounts in Google Colab that have access to the shared Drive path.

The genetic algorithm relies on a random sampler to promote searching parameters.

Human evaluation is required for all BASALT environments, a usage detail worth taking into consideration carefully.
The metric I used for successful attempts with the FindCave environment was early exits from the testing session.
This is identifiable as the agent throwing a snowball, which will termination the current test.
The FindCave dataset includes this action as an intended action when a cave has been found.
I opted to run ten trials with each model to see the overall performance of the model.

Once a metric for human evaluation has been established, the video files for each test of each model can be used to evaluate each model.
The results can be used to filter a certain proportion of the hyperparameters (stored in modelinfo.csv) for the next generation.
Seeding the next generation must be done by manually updating the *samples.csv* file.

### Results

Due to time constraints (covered in more detail in the *Discussion* section) only one iteration of the model could be run.
Here are the results of this attempt with the scoring system defined in the *Methods and Procedure* section:

| Model | Score | Video associated |
| ----- | ----- | ---------------- |
| A† #1	| 1	| #10 |
| A #2	| 0	| N/A |
| A #3 	| 0	| N/A |
| A #4	| 0	| N/A |
| A #5	| 0	| N/A |
| A #6	| 0	| N/A |
| D #1	| 0	| N/A |
| D #2	| 0	| N/A |
| D #3	| 0	| N/A |
| D #4	| 0	| N/A |
| D #5	| 0	| N/A |
| D #6	| 0	| N/A |
| D #7	| 0	| N/A |
| D2 #1	| 0	| N/A |
| D2 #2	| 0	| N/A |
| D2 #3	| 0	| N/A |
| D2 #4	| 0	| N/A |
| D2 #5	| 0	| N/A |
| Host #1	|	0	| N/A	|
| Host #2	|	0	| N/A |
| Host #3	|	0	| N/A |
| Host #4	|	0	| N/A	|
| Host #5	|	0	| N/A	|
| Host #6	|	0	| N/A	|
| Side #1	|	0	| N/A	|
| Side #2	| 0	| N/A	|
| Side #3 | 0 |	N/A |
| Side #4	| 0	| N/A |
| Side #5	|	0 |	N/A	|

† A and D are the initials of friends of mine I was able to borrow computers from for this work.

#### Success model and video

These are published as *bestmodel.pth* and *success.mp4* in this folder.

### Discussion

The primary focus of this section is to cover many of the key issues with this approach.

#### Time constraints

Running a genetic algorithm approach with the BASALT environment is extremely time-intensive.
Even without the need to restart the runtime (a common issue when running on Colab), the average execution time for training and testing a new model is around 50 minutes.
Most of this time is spent on testing (~40 minutes for 10 test trials).

Each model produces ten videos (~10 minutes of video content to evaluate), and even taking into consideration that only part of the videos needs to be watched to evaluate the model under the criteria defined in the *Methods and Procedure* section, recording and evaluating takes more than the length of the video in my experience.

A more generous scoring scheme would require even further time to evaluate performance.

All told, for the 26 models I tested, the total time on just this single generation I spent was:
* ~30 compute hours across 5 computers (approx. 6 hours of micromanagement also required during this to prevent inactivity disconnections)
* ~6 evaluation hours watching video and scoring
* ~1 hour reorganizing files related to a bug documented in the notebook file

The problem of using a genetic algorithm for this task comes in with trying to do this several times in a two-week sprint.
Even if compute time could be ignored, evaluation time is too demanding to attempt double-digits generations.

#### Accuracy

Without extensive training, imitation learning with the BASALT FindCave environment performs very poorly.

Only one clear success out of 260 attempts makes it difficult to justify the time investment required for this approach.

#### Scoring

Scoring the performance of the agent is difficult because of the openness of the problem.
The scoring system I adopted aimed to prioritize the time to evaluate, as partial scoring requires:
* a full analysis of each video
* deliberation on what counts as being "in a cave"
* considerations for partial points (surviving the test session, depth of cave explored, etc.)
All of which could dramatically increase the amount of time to score.

If time is not of an immediate concern, however, a partial scoring scheme would be advisable to allow more granular improvement.
It is difficult to progress with a single success.

#### Recommendations for further use of the BASALT datasets

The BASALT datasets are still potentially useful for this project, even if the BASALT environment is difficult to use.
A potential application of the BASALT dataset is for *transfer learning*, to train a model to find caves and then train it for the associated cave-related task.
This is an approach that I was unable to test during this sprint but could improve Stone collection performance.










