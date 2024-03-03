from multiprocessing import Process, Queue, Pipe
import sys
import os

from ML4MC_generated import Ui_MainWindow
from controller import AgentController
from emitter import Emitter
from gui import GUI
from ml4mc_env import ML4MCEnv

DIRNAME = os.path.dirname(__file__)

OBS_QUEUE = Queue()
OBJECTIVE_QUEUE = Queue()
RESTART_QUEUE = Queue()
QUIT_QUEUE = Queue()
NOTIFY_QUEUE = Queue()
PAUSE_QUEUE = Queue()

_ml4mc_env = ML4MCEnv(OBS_QUEUE, OBJECTIVE_QUEUE, RESTART_QUEUE, QUIT_QUEUE, PAUSE_QUEUE)
AI_CONTROLLER = AgentController(DIRNAME, NOTIFY_QUEUE, _ml4mc_env)
BACKEND_PROCESS = Process(target=AI_CONTROLLER.run)

def clean_up_agent():
    """
        Description:
            Function to clean up the agent process and queues.
    """
    # Clean up child process gracefully
    if BACKEND_PROCESS.is_alive():
        QUIT_QUEUE.put("QUIT") # Send signal to controller to quit
        BACKEND_PROCESS.join() # Wait for controller to finish
    
    # Clean up queues
    OBS_QUEUE.close()
    OBJECTIVE_QUEUE.close()
    RESTART_QUEUE.close()
    QUIT_QUEUE.close()
    NOTIFY_QUEUE.close()
    PAUSE_QUEUE.close()

def main():

    # Instantiate our classes
    emitter = Emitter(OBS_QUEUE, NOTIFY_QUEUE)
    gui = GUI(sys.argv, BACKEND_PROCESS, emitter, OBS_QUEUE, OBJECTIVE_QUEUE, RESTART_QUEUE, QUIT_QUEUE, PAUSE_QUEUE)
 
    # Application exit
    exit_code = gui.exec()
    clean_up_agent()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
