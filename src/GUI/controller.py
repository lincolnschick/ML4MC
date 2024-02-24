"""
Author: Adair Torres, Lincoln Schick
Description:
    AgentController object to handle interaction between GUI and Models.
    Loads environments and models accordingly.

    TODO:
        - Implement progress tracking for model goals.
        - Implement pausing / resuming actions for models.
        - Implement recording model action frames.
        - Implement toggling of individual scripts.
Last Modified: 2-6-2024
"""

import minerl
import gym
import os
import subprocess
from multiprocessing import Queue
import platform
from time import sleep
from model import Model
from minerl.herobraine.env_specs.ml4mc_survival_specs import ML4MCSurvival
from bc import ModelRunner
from ml4mc_env import ML4MCEnv, EpisodeFinishedException, ObjectiveChangedException, RestartException, QuitException

# Why can't Python be a normal language...
# Add paths of scripting directory to sys.path so we can import them
import sys, os
SCRIPT_DIR = os.path.dirname(os.path.abspath("script.py"))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from scripts.mine_to_surface import MineToSurfaceScript
from scripts.collect_diamonds import CollectDiamondsScript


class AgentController:
    def __init__(self, dirname: str, obs_q: Queue, objective_q: Queue, restart_q: Queue, quit_q: Queue):
        """
        Description:
            Construction for AgentController class. Contains member variables
            for tracking current environment, goal progress, queues for communication with GUI, 
            and state of the run (i.e. paused / running).
        """
        self._DIRNAME = dirname
        self._currentModel = None
        self._progress = 0           # For tracking goal progress
        self._paused = False         # Receiving signal to halt actions from the GUI
        self._displayInteractor = True # TODO: connect to GUI and set appropriate defaults
        self._displayAgentPOV = False # TODO: connect to GUI and set appropriate defaults

        self._queues = {
            "obs_q": obs_q,
            "objective_q": objective_q,
            "restart_q": restart_q,
            "quit_q": quit_q
        }

        self._modelDict = {}
        
        modelsList = [#("diamond_model.pth", "Obtain Diamond") TODO: fix when we have script section
                      ("iron_model.pth", "Obtain Iron"),
                      ("surive_model_placeholder", "Survive"),
                      ("wood_model.pth", "Gather Wood"),
                      #("stone_model_placeholder", "Gather Stone"),
                      ("enemies_model_placeholder", "Defeat Enemies")]
        
        for pair in modelsList:
            modelPath = os.path.join(self._DIRNAME, "models", pair[0])
            newModel = Model(pair[0], pair[1], modelPath)
            self._modelDict[newModel.get_objective()] = newModel

        self._scriptDict = { # TODO: change to name of scripts. This is just for testing
            "Obtain Diamond": CollectDiamondsScript,
            "Gather Stone": MineToSurfaceScript,
        }
        
        # Set the current model to the default
        self._currentModel = self._modelDict["Obtain Iron"] # TODO: change to diamond
        
        # Initialize and register custom environments
        ml4mcSurvival = ML4MCSurvival()
        ml4mcSurvival.register()

        self._ml4mc_env = ML4MCEnv(self._displayAgentPOV, **self._queues) # Wrapper for the MineRL environment

    def run_episode(self):
        """
        Description:
            Function to run a single episode of the agent in the environment.
            Terminates when the episode is finished or the user interrupts.
        """
        runner = ModelRunner(self._currentModel, self._ml4mc_env) # Default to running with default BC model
        while True:
            try:
                runner.run()
            except ObjectiveChangedException as e:
                runner = self.update_runner(e.objective)
    
    def run(self):
        """
        Description:
            Main loop for the agent controller, which is run as a separate process.
            Continues to run episodes until the user quits the program.
        """
        self._ml4mc_env.start()
        while True:
            # Set up environment from specification
            self._ml4mc_env.reset()
            
            if self._displayInteractor:
                self.launch_interactor()
            
            try:
                self.run_episode()
            except (EpisodeFinishedException, RestartException):
                self.quit_interactor() # Quit the interactor if it's running; it must be quit before the environment can be reset
            except QuitException:
                self.quit_interactor()
                break
    
    def launch_interactor(self):
        """
        Description:
            Function to connect to the agent's LAN server using the minerl interactor.
        """
        subprocess.call(["python", "-m", "minerl.interactor", "5656"])
    
    def quit_interactor(self):
        """
        Description:
            Function to quit the minerl interactor window, does nothing if the interactor is not running.
        """
        try:
            if platform.system() == "Darwin" or platform.system() == "Linux": # MacOS or Linux
                # Get the PID of the interactor process (always listening on port 31415)
                pid = int(subprocess.check_output(["lsof", "-ti:31415"]).strip())
                subprocess.call(["kill", pid]) # Send SIGTERM to the interactor
            else: # Windows
                # TODO: test this on Windows, it almost certainly won't work as is
                pid = int(subprocess.check_output(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command",
                                                "(Get-NetTCPConnection -LocalPort 31415).OwningProcess"]).strip())
                subprocess.call(["taskkill", "/pid", pid])
        except Exception as e:
            print("Error quitting interactor (expected if interactor is not running): ", e)

    def update_runner(self, objective):
        """
        Description:
            Function to handle items in the objective queue, used to update the current objective and model.
        """
        if objective in self._modelDict:
            self._currentModel = self._modelDict[objective]
            return ModelRunner(self._currentModel, self._ml4mc_env)
        else:
            return self._scriptDict[objective](self._ml4mc_env)