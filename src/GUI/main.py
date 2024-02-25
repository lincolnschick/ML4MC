from PyQt6 import QtCore, QtGui, QtWidgets
from ML4MC_generated import Ui_MainWindow
from functools import partial
from multiprocessing import Process, Queue, Pipe
from controller import AgentController
import sys
import os

DIRNAME = os.path.dirname(__file__)
OBS_QUEUE = Queue()
OBJECTIVE_QUEUE = Queue()
QUIT_QUEUE = Queue()
RESTART_QUEUE = Queue()
AI_CONTROLLER = AgentController(DIRNAME, OBS_QUEUE, OBJECTIVE_QUEUE, RESTART_QUEUE, QUIT_QUEUE)
BACKEND_PROCESS = Process(target=AI_CONTROLLER.run)

PLAINFONT = QtGui.QFont()
BOLDFONT = QtGui.QFont()
BOLDFONT.setBold(True)
STRIKEFONT = QtGui.QFont()
STRIKEFONT.setStrikeOut(True)

def apply_functionality(ui: Ui_MainWindow):
    """
        Description:
            Function to attach callback functions to GUI elements
            and set member variables to initial values.
    """
    ui.agentButton.clicked.connect(partial(start_agent_callback, ui))
    ui.resetEnvironmentButton.clicked.connect(partial(reload_environment_callback, ui))

    ui.currentObjectiveWidget = ui.ironRadio
    ui.ironRadio.clicked.connect(partial(objective_clicked_callback, ui, widget=ui.ironRadio))
    ui.woodRadio.clicked.connect(partial(objective_clicked_callback, ui, widget=ui.woodRadio))
    ui.combatRadio.clicked.connect(partial(objective_clicked_callback, ui, widget=ui.combatRadio))
    ui.surviveRadio.clicked.connect(partial(objective_clicked_callback, ui, widget=ui.surviveRadio))
    
    ui.activeScriptWidget = None
    ui.diamondScriptRadio.clicked.connect(partial(execute_diamond_script))
    ui.stoneScriptRadio.clicked.connect(partial(continuous_script_callback, ui, widget=ui.diamondScriptRadio))

def execute_diamond_script():
    OBJECTIVE_QUEUE.put("Collect Diamond")

def start_agent_callback(ui: Ui_MainWindow):
    """
        Description:
            Callback function to start the minerl
            environment process and disable the 
            "Start Agent" button until the process
            ends or joins.
    """
    print(f"Starting minerl environment and agent...")
    ui.resetEnvironmentButton.setEnabled(True)
    ui.agentButton.setEnabled(False)
    BACKEND_PROCESS.start()

def reload_environment_callback(ui: Ui_MainWindow):
    """
        Description:
            Function to reload the custom ML4MC environment after
            user input via GUI.
    """
    ui.resetEnvironmentButton.setEnabled(False)
    print(f"Reloading minerl environment...")
    
    # Send message to controller to restart the environment
    RESTART_QUEUE.put("RESTART")
    ui.resetEnvironmentButton.setEnabled(True)

def objective_clicked_callback(ui: Ui_MainWindow, widget):
    """
        Description:
            Callback function that updates the selected AI
            objective and relevant UI elements.
        Inputs:
            widget - The GUI element that triggered the event.
        Output: None
    """
    newObjective = widget.text().replace('\n', ' ')
    print(f"objective_clicked_callback triggered on {newObjective}")

    # plainFont = QtGui.QFont()
    ui.currentObjectiveWidget.setFont(PLAINFONT)
    ui.currentObjectiveWidget.setEnabled(True)     # Enable the old objective widget


    OBJECTIVE_QUEUE.put(newObjective)               # Update the controller
    ui.progressBar.setValue(0)
    ui.currentObjectiveLabel.setText(f"Goal: <b>{newObjective}</b>")
    ui.currentObjectiveLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    ui.currentObjectiveWidget = widget            # Update current objective widget

    # boldFont = QtGui.QFont()
    # boldFont.setBold(True)
    ui.currentObjectiveWidget.setFont(BOLDFONT)
    ui.currentObjectiveWidget.setEnabled(False)    # Disable current objective widget
    print(f"Changed objective to {newObjective}")

def continuous_script_callback(ui: Ui_MainWindow, widget):
    """
        Description:
            Callback function that toggles scripts and updates relevant UI elements.
        Inputs:
            widget - The GUI element that triggered the event and should be toggled.
        Output: None
    """
    script = widget.text().replace('\n', ' ')
    print(f"continuous_script_callback triggered on {script}")

    # plainFont = QtGui.QFont()
    ui.activeScriptWidet.setFont(PLAINFONT)

    # boldFont = QtGui.QFont()
    # boldFont.setBold(True)
    widget.setFont(BOLDFONT)

    ui.activeScriptWidget = widget
    ui.stopScriptButton.setEnabled(True)

def stop_continuous_callback(ui: Ui_MainWindow):
    """
        Description:
            Callback function that toggles scripts and updates relevant UI elements.
        Inputs:
            widget - The GUI element that triggered the event and should be toggled.
        Output: None
    """
    print("stop_continuous_callback triggered")

    ui.activeScriptWidget.setFont(PLAINFONT)
    ui.stopScriptButton.setEnabled(False)

def execute_script_callback(ui: Ui_MainWindow, widget):
    """
        Description:
            Callback function that toggles scripts and updates relevant UI elements.
        Inputs:
            widget - The GUI element that triggered the event and should be toggled.
        Output: None
    """
    scriptToggled = widget.text().replace('\n', ' ')
    print(f"script_toggled_callback triggered on {scriptToggled}")

def script_toggled_callback(ui: Ui_MainWindow, widget):
    """
        Description:
            Callback function that toggles scripts and updates relevant UI elements.
        Inputs:
            widget - The GUI element that triggered the event and should be toggled.
        Output: None
    """
    scriptToggled = widget.text().replace('\n', ' ')
    print(f"script_toggled_callback triggered on {scriptToggled}")

    if widget.isChecked():
        plainFont = QtGui.QFont()
        widget.setFont(plainFont)
        print(scriptToggled + " scripts toggled on.")

        # Send signal to controller to turn specific script off
    else:
        strikeFont = QtGui.QFont()
        strikeFont.setStrikeOut(True)
        widget.setFont(strikeFont)
        print(scriptToggled + " scripts toggled off.")

        # Send signal to controll to turn specific script on.

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

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    apply_functionality(ui)
    MainWindow.show()
    exit_code = app.exec()
    clean_up_agent()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
