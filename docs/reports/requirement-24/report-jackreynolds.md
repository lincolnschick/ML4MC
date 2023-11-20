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

Once a metric for human evaluation has been established, the video files for each test of each model can be used to evaluate each model.
The results can be used to filter a certain proportion of the hyperparameters (stored in modelinfo.csv) for the next generation.
Seeding the next generation must be done by manually updating the *samples.csv* file.

### Results

| Model | Score | Video associated
| A #1	| 1	| #10 |
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
