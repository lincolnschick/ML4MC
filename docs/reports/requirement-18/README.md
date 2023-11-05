# Competing Model Training

Initial testing using the optimal TreeChop environment parameters from last sprint as a starting point showed that increasing the number of epochs significantly (to 30-70) resulted in the agent frequently freezing up and stopping entirely. On the other hand, training on just a few epochs showed more random movement/actions. 

We decided to test models trained on the parameters {'learning_rate': 0.00028, 'epochs': 8, 'batch_size': 32} as this gave the best results with our testing. However, additional optimization is certainly possible and will be explored in the future.

In total, 17 models were trained on this set of parameters (batch size, learning rate, epochs).

Training method was *Behavioral Cloning* as used in previous requirements.

Some videos were lost during the process since multiple machines were used at once, so not all runs have all 10 videos.

Results were validated by inspection of each video.

Inspection based on the quality of the video was not perfect because of lighting and resolution issues.

## Featured in this folder

#### Notebook

*FindCaveTestAll.ipynb*

The notebook file used to run the model.

#### Optimal

*bestmodel.pth*

The one and only model that recognized it was in a cave twice.
This gives it the best accuracy of around 20% success in identifying caves.
The average among all models, for comparison, sat around 4% success.

*bestmodel_success1.mp4* and *bestmodel_success2.mp4*

Video of the two successes for the best model.

#### Suboptimal, but noteworthy

*goodnavigation.pth*

This model did not successfully recognize it was in a cave, but navigated caves really well.
Its searching capabilities could be useful for gathering stone or ore.

*goodnavigation.mp4*

Video of the navigation done by this model.

#### Examples of common failures

*lava.mp4*, *water.mp4*, *ravine.mp4*

Very common sources of failure for the model (more common than correct identification) were environmental hazards.
Behavioral Cloning does not disincentivize avoiding these, so most models failed to avoid them.
