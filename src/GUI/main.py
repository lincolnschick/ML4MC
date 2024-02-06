from PyQt6 import QtCore, QtGui, QtWidgets
from gui_design import Ui_MainWindow
from functools import partial
from multiprocessing import Process, Queue
from controller import AgentController
import sys
import os

DIRNAME = os.path.dirname(__file__)
OBS_QUEUE = Queue()
OBJECTIVE_QUEUE = Queue()
AI_CONTROLLER = AgentController(DIRNAME, OBS_QUEUE, OBJECTIVE_QUEUE)
BACKEND_PROCESS = Process(target=AI_CONTROLLER.run)

def apply_functionality(ui: Ui_MainWindow):
    """
        Description:
            Function to attach callback functions to GUI elements.
    """
    ui.agentButton.clicked.connect(partial(start_agent_callback, ui))
    ui.resetEnvironmentButton.clicked.connect(partial(reload_environment_callback, ui))

    ui.currentObjectiveWidget = ui.diamondRadio
    ui.ironRadio.clicked.connect(partial(objective_clicked_callback, ui, widget=ui.ironRadio))
    ui.woodRadio.clicked.connect(partial(objective_clicked_callback, ui, widget=ui.woodRadio))
    ui.stoneRadio.clicked.connect(partial(objective_clicked_callback, ui, widget=ui.stoneRadio))
    ui.combatRadio.clicked.connect(partial(objective_clicked_callback, ui, widget=ui.combatRadio))
    ui.diamondRadio.clicked.connect(partial(objective_clicked_callback, ui, widget=ui.diamondRadio))
    ui.surviveRadio.clicked.connect(partial(objective_clicked_callback, ui, widget=ui.surviveRadio))
    
    ui.armorCheckBox.clicked.connect(partial(script_toggled_callback, ui, widget=ui.armorCheckBox))
    ui.weaponsCheckBox.clicked.connect(partial(script_toggled_callback, ui, widget=ui.weaponsCheckBox))
    ui.buildingCheckBox.clicked.connect(partial(script_toggled_callback, ui, widget=ui.buildingCheckBox))
    ui.lightingCheckBox.clicked.connect(partial(script_toggled_callback, ui, widget=ui.lightingCheckBox))
    ui.smeltingCheckBox.clicked.connect(partial(script_toggled_callback, ui, widget=ui.smeltingCheckBox))
    ui.craftingCheckBox.clicked.connect(partial(script_toggled_callback, ui, widget=ui.craftingCheckBox))

def start_agent_callback(ui: Ui_MainWindow):
    print(f"Starting minerl environment and agent...")
    BACKEND_PROCESS.start()
    ui.resetEnvironmentButton.setEnabled(True)
    ui.agentButton.setEnabled(False)

def reload_environment_callback(ui: Ui_MainWindow):
    """
        Description:
            Function to reload the custom ML4MC environment after
            user input via GUI.
    """
    print(f"Reloading minerl environment...")
    # Pass some flag to controller process to fire AI_CONTROLLER.reset_environment()

    ui.resetEnvironmentButton.setEnabled(False)

    # Disable button until controller sends back a signal that it's "okay" to do so

    ui.resetEnvironmentButton.setEnabled(True)


def objective_clicked_callback(ui: Ui_MainWindow, widget):
    """
        Description: Callback function that updates the selected AI objective and relevant UI elements.
        Inputs:
            widget - The GUI element that triggered the event.
        Output: None
    """
    newObjective = widget.text().replace('\n', ' ')
    print(f"objective_clicked_callback triggered on {newObjective}")

    plainFont = QtGui.QFont()
    ui.currentObjectiveWidget.setFont(plainFont)
    ui.currentObjectiveWidget.setEnabled(True)     # Enable the old objective widget


    OBJECTIVE_QUEUE.put(newObjective)               # Update the controller
    ui.progressBar.setValue(0)
    ui.currentObjectiveLabel.setText(f"Goal: <b>{newObjective}</b>")
    ui.currentObjectiveLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    ui.currentObjectiveWidget = widget            # Update current objective widget

    boldFont = QtGui.QFont()
    boldFont.setBold(True)
    ui.currentObjectiveWidget.setFont(boldFont)
    ui.currentObjectiveWidget.setEnabled(False)    # Disable current objective widget
    print(f"Changed objective to {newObjective}")

def script_toggled_callback(ui: Ui_MainWindow, widget):
    """
        Description: Callback function that toggles scripts and updates relevant UI elements.
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

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    apply_functionality(ui)
    MainWindow.show()
    exit_code = app.exec()
    if BACKEND_PROCESS.is_alive(): # If the backend process is still running, end it with the UI
        BACKEND_PROCESS.terminate()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
