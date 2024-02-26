from PyQt6 import QtCore, QtGui, QtWidgets
from multiprocessing import Process, Queue
from functools import partial
import math


from ML4MC_generated import Ui_MainWindow
from emitter import Emitter

PLAINFONT = QtGui.QFont()
BOLDFONT = QtGui.QFont()
BOLDFONT.setBold(True)
STRIKEFONT = QtGui.QFont()
STRIKEFONT.setStrikeOut(True)

class GUI():
    def __init__(self, args, backend: Process, emitter: Emitter, obs_q: Queue, objective_q: Queue, restart_q: Queue, quit_q: Queue):
        self._backend = backend
        self._emitter = emitter
        self._obs_q = obs_q
        self._objective_q = objective_q
        self._restart_q = restart_q
        self._quit_q = quit_q
        
        self._app = QtWidgets.QApplication(args)
        self._MainWindow = QtWidgets.QMainWindow()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self._MainWindow)
        self.apply_functionality()
        self._MainWindow.show()

        self._exit_code = self._app.exec()

    def apply_functionality(self):
        """
            Description:
                Function to attach callback functions to GUI elements
                and set member variables to initial values.
        """
        self._ui.agentButton.clicked.connect(self.start_agent)
        self._ui.resetEnvironmentButton.clicked.connect(self.reload_environment_callback)

        self._ui.currentObjectiveWidget = self._ui.ironRadio
        self._ui.ironRadio.clicked.connect(partial(self.objective_clicked, widget=self._ui.ironRadio))
        self._ui.woodRadio.clicked.connect(partial(self.objective_clicked, widget=self._ui.woodRadio))
        self._ui.combatRadio.clicked.connect(partial(self.objective_clicked, widget=self._ui.combatRadio))
        self._ui.surviveRadio.clicked.connect(partial(self.objective_clicked, widget=self._ui.surviveRadio))
        
        # Scripts Functionality
        self._ui.activeScriptWidget = None
        self._ui.currentScript = ""
        self._ui.stopScriptButton.clicked.connect(self.stop_script)
            # Continuous Scripts
        self._ui.diamondScriptButton.clicked.connect(partial(self.start_script, widget=self._ui.diamondScriptButton))
        self._ui.stoneScriptButton.clicked.connect(partial(self.start_script, widget=self._ui.stoneScriptButton))
            # Execute Once Scripts
        self._ui.surfaceScriptButton.clicked.connect(partial(self.start_script, widget=self._ui.surfaceScriptButton))
        self._ui.depthScriptButton.clicked.connect(partial(self.start_script, widget=self._ui.depthScriptButton))


    def start_agent(self):
        """
        Description:
            Callback function to start the minerl environment process and
            disable the "Start Agent" button until the process ends or joins.
        """
        print("start_agent triggered")
        self._ui.resetEnvironmentButton.setEnabled(True)
        self._ui.diamondScriptButton.setEnabled(True)
        self._ui.stoneScriptButton.setEnabled(True)
        self._ui.surfaceScriptButton.setEnabled(True)
        self._ui.depthScriptButton.setEnabled(True)
        self._ui.agentButton.setEnabled(False)
        self._emitter.start()
        self._backend.start()
        self._emitter.data_available.connect(self.update_statistics)

    def update_statistics(self):
        """
        Description:
            Function to update the GUI's display of the agent's statistics,
            including life, food, x_pos, y_pos, and z_pos.
        """
        obs = self._obs_q.get()
        self._ui.xCoordLabel.setText("X: " + str(int(obs['location_stats']['xpos'])))
        self._ui.yCoordLabel.setText("Y: " + str(int(obs['location_stats']['ypos'])))
        self._ui.zCoordLabel.setText("Z: " + str(int(obs['location_stats']['zpos'])))
        self._ui.healthLabel.setText(str(obs['life_stats']['life']))
        self._ui.hungerLabel.setText(str(obs['life_stats']['food']))
    
    def enable_restart(self):
        """
        Description:
            Function to enable the Restart Environment button once given
            the signal it is safe to do so.
        """
        print("enable_restart triggered")
        self._ui.resetEnvironmentButton.setEnabled(True)

    def script_finished(self):
        """
        Description:
            Function to restore the completed script's text and restore
            the previously running objective.
        """
        print("script_finished triggered")
        self.restore_script_text()
        oldObjective = self._ui.currentObjectiveWidget.text().replace('\n', ' ')
        self._objective_q.put(oldObjective)

    def handle_emitter(self, text):
        """
        Description:
            Callback function to read the text sent by the emitter and
            call the appropriate function for the GUI.
        """
        if text == "obs sent":
            self.update_statistics()
        elif text == "restart finished":
            self.enable_restart()
        elif text == "script finished":
            self.script_finished()

    def reload_environment_callback(self):
        """
            Description:
                Function to reload the custom ML4MC environment after user
                input via GUI.
        """
        print("reload_environment triggered")
        self._ui.resetEnvironmentButton.setEnabled(False)
        
        # Send message to controller to restart the environment
        self._restart_q.put("RESTART")

    def objective_clicked(self, widget):
        """
            Description:
                Callback function that updates the selected AI objective and
                relevant UI elements.
            Inputs:
                widget - The GUI element that triggered the event.
            Output: None
        """
        newObjective = widget.text().replace('\n', ' ')
        print(f"objective_clicked triggered on {newObjective}")

        # Restore text and disable stop script button if a script was running
        if self._ui.activeScriptWidget != None:
            self.restore_script_text()
            self._ui.stopScriptButton.setEnabled(False)

        # Restore old objective widget text to normal and enable
        self._ui.currentObjectiveWidget.setFont(PLAINFONT)
        self._ui.currentObjectiveWidget.setEnabled(True)

        self._objective_q.put(newObjective)     # Update the controller

        # Update the progress bar and goal text
        self._ui.progressBar.setValue(0)
        self._ui.currentObjectiveLabel.setText(f"Goal: <b>{newObjective}</b>")
        self._ui.currentObjectiveLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Update current object widget tracker and disable
        self._ui.currentObjectiveWidget = widget
        self._ui.currentObjectiveWidget.setFont(BOLDFONT)
        self._ui.currentObjectiveWidget.setEnabled(False)

    def start_script(self, widget):
        """
            Description:
                Callback function that sets the triggering scripts as
                the current task for the agent.
            Inputs:
                widget - The GUI element that triggered the event.
            Output: None
        """
        script = widget.text().replace('\n',  ' ')
        print(f"start_script triggered on {script}")

        if self._ui.activeScriptWidget != None:
            self.restore_script_text()

        self._objective_q.put(script)

        widget.setFont(BOLDFONT)
        widget.setText("Running...")
        self._ui.activeScriptWidget = widget
        self._ui.activeScriptWidget.setEnabled(False)
        self._ui.currentScript = script
        self._ui.stopScriptButton.setEnabled(True)

    def stop_script(self):
        """
            Description:
                Callback function that stops the currently running script
                and restores the previously selected objective.
        """
        print("stop_script triggered")

        oldObjective = self._ui.currentObjectiveWidget.text().replace('\n', ' ')
        self._objective_q.put(oldObjective)
        self.restore_script_text()
        self._ui.activeScriptWidget = None
        self._ui.currentScript = ""
        self._ui.stopScriptButton.setEnabled(False)

    def restore_script_text(self):
        self._ui.activeScriptWidget.setFont(PLAINFONT)
        self._ui.activeScriptWidget.setText(self._ui.currentScript.replace(' ', '\n', 1))
        self._ui.activeScriptWidget.setEnabled(True)

    def exec(self):
        return self._exit_code