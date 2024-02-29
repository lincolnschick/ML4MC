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
from model import Model
from gui import RESTART_FINISHED_MSG
from minerl.herobraine.env_specs.ml4mc_survival_specs import ML4MCSurvival
from bc import ModelRunner
from ml4mc_env import ML4MCEnv, EpisodeFinishedException, ObjectiveChangedException, RestartException, QuitException

# Why can't Python be a normal language...
# Add paths of scripting directory to sys.path so we can import them
import sys, os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from scripts.mine_to_surface import MineToSurfaceScript
from scripts.collect_diamonds import CollectDiamondsScript


class AgentController:
    def __init__(self, dirname: str, notify_q: Queue, obs_q: Queue, objective_q: Queue, restart_q: Queue, quit_q: Queue):
        """
        Description:
            Construction for AgentController class. Contains member variables
            for tracking current environment, goal progress, queues for communication with GUI, 
            and state of the run (i.e. paused / running).
        """
        self._DIRNAME = dirname
        self._currentModel = None
        self._progress = 0           # For tracking goal progress
        self._notify_q = notify_q    # Queue to send simple messages to the GUI

        self._modelDict = {}
        
        modelsList = [("iron_model.pth", "Obtain Iron"),
                      ("surive_model_placeholder", "Survive"),
                      ("wood_model.pth", "Gather Wood"),
                      ("enemies_model_placeholder", "Defeat Enemies")]
        
        for pair in modelsList:
            modelPath = os.path.join(self._DIRNAME, "models", pair[0])
            newModel = Model(pair[0], pair[1], modelPath)
            self._modelDict[newModel.get_objective()] = newModel

        self._scriptDict = {
            "Collect Diamond": CollectDiamondsScript,
            "Mine to Surface": MineToSurfaceScript,
        }

        # Set the current model to the default
        self._currentModel = self._modelDict["Obtain Iron"]
        
        # Initialize and register custom environments
        ml4mcSurvival = ML4MCSurvival()
        ml4mcSurvival.register()

        self._ml4mc_env = ML4MCEnv(obs_q, objective_q, restart_q, quit_q) # Wrapper for the MineRL environment

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
            
            # ML4MCEnv should be source of truth for displaying interactor because it can check the queues more frequently
            if self._ml4mc_env.display_interactor:
                self.launch_interactor()
            
            # Set display POV based on current UI settings on reset
            self._ml4mc_env.set_display_pov()

            # Notify the GUI that the restart has finished
            # This could also be the first launch, but it won't cause any issues
            self._notify_q.put(RESTART_FINISHED_MSG)
            
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
            return self._scriptDict[objective](self._ml4mc_env, self._notify_q)