"""
Author: Adair Torres
Description:
    ModelSwapper object to handle interaction between GUI and Models.
    Loads environments and models accordingly.

    TODO:
        - Implement an actual model for testing.
        - Implement progress tracking for model goals.
        - Implement pausing / resuming actions for models.
        - Implement recording model action frames.
        - Implement toggling of individual scripts.
Last Modified: 1-28-2024
"""

import minerl
import gym
import os

from model import Model
from minerl.herobraine.env_specs.ml4mc_survival_specs import ML4MCSurvival

class ModelSwapper():
    def __init__(self, dirname):
        """
        Description:
            Construction for ModelSwapper class. Contains member variables
            for tracking current environment, goal progress, and state of 
            the run (i.e. paused / running).
        """
        self._DIRNAME = dirname
        self._loadedEnvironment = None
        self._currentModel = None
        self._progress = 0           # For tracking goal progress
        self._paused = False         # Receiving signal to halt actions from the GUI

        self._modelDict = {}
        
        modelsList = [("diamond_model_placeholder", "Obtain Diamond"),
                      ("iron_model_placeholder", "Obtain Iron"),
                      ("surive_model_placeholder", "Survive"),
                      ("wood_model_placeholder", "Gather Wood"),
                      ("stone_model_placeholder", "Gather Stone"),
                      ("enemies_model_placeholder", "Defeat Enemies")]
        
        for pair in modelsList:
            modelPath = os.path.join(self._DIRNAME, "models", pair[0])
            newModel = Model(pair[0], pair[1], modelPath)
            self._modelDict[newModel.get_objective()] = newModel

        self._currentModel= self._modelDict["Obtain Diamond"]
        
        # Initialize and register custom environments
        ml4mcSurvival = ML4MCSurvival()
        ml4mcSurvival.register()
    
    def load_default_environment(self):
        """
        Description:
            Load the custom ML4MCSurvival-v0 environment. This environment
            is regularly updated to include observations needed by models,
            but not offered as part of the standard minerl environments.
        """
        self._loadedEnvironment = gym.make('ML4MCSurvival-v0')
        self._loadedEnvironment.reset()
        return
    
    def reset_environment(self):
        """
        Description:
            Reset the current environment.
        """
        self._loadedEnvironment.reset()
        return

    def load_model(self, objective):
        """
        Description:
            Load the given model to begin running based on the given objective.
        """
        if objective != self._currentModel.get_objective():
            self._currentModel = self._modelDict[objective]
            self._currentModel.load()
            return
        else:
            raise RuntimeError(f"Model for {objective} is already loaded.")