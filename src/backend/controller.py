"""
Author: Adair Torres, Lincoln Schick
Description:
    AgentController object to handle interaction between GUI and Models.
    Loads environments and models accordingly.

    TODO:
        - Implement progress tracking for model goals.
Last Modified: 3-23-2024
"""

import minerl
import gym

import subprocess
from multiprocessing import Queue
import platform
from minerl.herobraine.env_specs.ml4mc_survival_specs import ML4MCSurvival

from backend.config import Objective, Script, Message
from backend.ml4mc_env import ML4MCEnv, EpisodeFinishedException, ObjectiveChangedException, RestartException, QuitException
from backend.model import Model
from backend.bc_models import IronModel, StoneModel, WoodModel
from backend.rl_models import FightEnemiesModel
from backend.scripts import MineToSurfaceScript, CollectDiamondsScript, GatherStoneScript, CraftPickaxeScript, CraftSwordScript

# # Why can't Python be a normal language...
# # Add paths of scripting directory to sys.path so we can import them
# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))

class AgentController:
    def __init__(self, notify_q: Queue, interact_q: Queue, ml4mc_env: ML4MCEnv):
        """
        Description:
            Construction for AgentController class. Contains member variables
            for tracking current environment, goal progress, queues for communication with GUI, 
            and state of the run (i.e. paused / running).
        Inputs / Member Variables:
            notify_q: Queue handling GUI notifications and messages
            interact_q: Queue handling signals to load or skip interactor startup
            ml4mc_env: The minerl environment wrapper to load
        """
        self._currentModel = None
        self._progress = 0           # For tracking goal progress
        self._notify_q = notify_q    # Queue to send simple messages to the GUI
        self._interact_q = interact_q   # Queue for signals to load or skip interactor loading
        self._interact = False  # Default
        self.interactor_pid = None

        self._modelDict: dict[int, Model] = {
            Objective.IRON: IronModel,
            Objective.STONE: StoneModel,
            Objective.WOOD: WoodModel,
            Objective.ENEMIES: FightEnemiesModel,
        }

        self._scriptDict = {
            Script.DIAMOND: CollectDiamondsScript,
            Script.SURFACE: MineToSurfaceScript,
            Script.STONE: GatherStoneScript,
            Script.PICKAXE: CraftPickaxeScript,
            Script.SWORD: CraftSwordScript,
        }

        # Set the current model to the default
        self._currentModel = self._modelDict[Objective.WOOD]

        # Initialize and register custom environments
        ml4mcSurvival = ML4MCSurvival()
        ml4mcSurvival.register()

        self._ml4mc_env = ml4mc_env # Wrapper for the MineRL environment

    def run_episode(self):
        """
        Description:
            Function to run a single episode of the agent in the environment.
            Terminates when the episode is finished or the user interrupts.
        """
        runner = self._currentModel(self._ml4mc_env) # Default to running with default BC model
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

            # Load interactor based on current UI settings on reset
            if not self._interact_q.empty():
                while not self._interact_q.empty():
                    self._interact = self._interact_q.get()
            if self._interact:
                self.launch_interactor()
            
            # Set display POV based on current UI settings on reset
            self._ml4mc_env.set_display_pov()

            # Notify the GUI that the restart has finished
            # This could also be the first launch, but it won't cause any issues
            self._notify_q.put(Message.RESTART_FINISHED)
            
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
            Function to connect to the agent's LAN server using the minerl interactor
            and record the process ID to be used to quit the interactor later.
        """
        # Launch the interactor and capture output to get the port number
        proc = subprocess.run(["python", "-m", "minerl.interactor", "5656"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        output = proc.stdout
        
        # Get the last 20 lines of the output as this is where the port number is printed
        last_lines = output.splitlines()[-20:]
        MALMO_ENV_PORT_STR = "***** Start MalmoEnvServer on port "
        port = None
        for line in last_lines:
            if MALMO_ENV_PORT_STR not in line:
                continue
            port = int(line.split(MALMO_ENV_PORT_STR)[-1])
            break
        
        if not port: # We find the port number since we just launched the interactor
            raise Exception("Failed to find port number in interactor output", last_lines)

        if platform.system() == "Darwin" or platform.system() == "Linux": # MacOS or Linux
            self.interactor_pid = subprocess.check_output(["lsof", f"-ti:{port}"]).decode().strip()
        else: # Windows
            pids = subprocess.check_output(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command",
                                               f"(Get-NetTCPConnection -LocalPort {port}).OwningProcess"]).decode()
            self.interactor_pid = pids.split()[0]
            # Get parent of main interactor process
            self.interactor_pid = subprocess.check_output(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command",
                                               f'wmic process where ("processid={self.interactor_pid}") get parentprocessid']).decode().strip().split()[-1]
            # Get grandparent of main interactor process (needed to prevent the Windows bug causing the interactor to repeatedly launch)
            self.interactor_pid = subprocess.check_output(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command",
                                               f'wmic process where ("processid={self.interactor_pid}") get parentprocessid']).decode().strip().split()[-1]

    
    def quit_interactor(self):
        """
        Description:
            Function to quit the minerl interactor window, does nothing if the interactor is not running.
        """
        if not self.interactor_pid:
            return

        try:
            if platform.system() == "Darwin" or platform.system() == "Linux": # MacOS or Linux
                subprocess.call(["kill", self.interactor_pid]) # Send SIGTERM to the interactor
            else: # Windows
                # Kill grandparent of main interactor process and all children
                subprocess.call(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command",
                                f"taskkill /pid {self.interactor_pid} /t /f"])
            self.interactor_pid = None
        except Exception as e:
            print("Error quitting interactor (expected if the interactor was closed manually): ", e)

    def update_runner(self, objective):
        """
        Description:
            Function to handle items in the objective queue, used to update the current objective and model.
        """
        if objective in self._modelDict:
            self._currentModel = self._modelDict[objective]
            return self._currentModel(self._ml4mc_env)
        else:
            return self._scriptDict[objective](self._ml4mc_env, self._notify_q)