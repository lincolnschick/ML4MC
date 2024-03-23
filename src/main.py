from multiprocessing import Process, Queue, Pipe
import sys
import os

from backend import Emitter, AgentController, ML4MCEnv, Message
from frontend import GUI, ScreenRecorder

def start_controller(obs_q: Queue,
                     obj_q: Queue,
                     restart_q: Queue,
                     quit_q: Queue,
                     pause_q: Queue,
                     pov_q: Queue,
                     notif_q: Queue,
                     interact_q: Queue):
        _ml4mc_env = ML4MCEnv(obs_q, obj_q, restart_q, quit_q, pause_q, pov_q)
        AI_CONTROLLER = AgentController(notif_q, interact_q, _ml4mc_env)
        AI_CONTROLLER.run()
        
def start_recorder(dirname: str, record_q: Queue):
    SCREEN_RECORDER = ScreenRecorder(dirname, record_q)
    SCREEN_RECORDER.run()

if __name__ == "__main__":
    DIRNAME = os.path.dirname(__file__)

    # Instantiate our Queues
    OBS_QUEUE = Queue()
    OBJECTIVE_QUEUE = Queue()
    RESTART_QUEUE = Queue()
    QUIT_QUEUE = Queue()
    NOTIFY_QUEUE = Queue()
    PAUSE_QUEUE = Queue()
    POV_QUEUE = Queue()
    INTERACTOR_QUEUE = Queue()
    RECORD_QUEUE = Queue()

    emitter = Emitter(OBS_QUEUE, NOTIFY_QUEUE)

    # Instantiate our Processes
    p_controller = Process(name="agent_controller",
                 target=start_controller,
                 args=(OBS_QUEUE,
                      OBJECTIVE_QUEUE,
                      RESTART_QUEUE,
                      QUIT_QUEUE,
                      PAUSE_QUEUE,
                      POV_QUEUE,
                      NOTIFY_QUEUE,
                      INTERACTOR_QUEUE,
                    )
                )
    p_recorder = Process(name="screen_recorder", target=start_recorder, args=(DIRNAME, RECORD_QUEUE,))

    # Instantiate GUI
    gui = GUI(sys.argv,
              p_controller,
              p_recorder,
              emitter,
              OBS_QUEUE,
              OBJECTIVE_QUEUE,
              RESTART_QUEUE,
              QUIT_QUEUE,
              PAUSE_QUEUE,
              POV_QUEUE,
              INTERACTOR_QUEUE,
              RECORD_QUEUE
            )
 
    # Application exit
    exit_code = gui.exec()

    # Clean up child process gracefully
    if p_controller.is_alive():
        QUIT_QUEUE.put(Message.QUIT) # Send signal to controller to quit
        p_controller.join() # Wait for controller to finish

    if p_recorder.is_alive():
        RECORD_QUEUE.put(Message.QUIT)
        p_recorder.join()
    
    # Clean up queues
    OBS_QUEUE.close()
    OBJECTIVE_QUEUE.close()
    RESTART_QUEUE.close()
    QUIT_QUEUE.close()
    NOTIFY_QUEUE.close()
    PAUSE_QUEUE.close()
    POV_QUEUE.close()
    INTERACTOR_QUEUE.close()
    RECORD_QUEUE.close()

    sys.exit(exit_code)
