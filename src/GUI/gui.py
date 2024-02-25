from PyQt6 import QtCore, QtGui, QtWidgets
from multiprocessing import Process, Queue
from functools import partial


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
        
        self._ui.activeScriptWidget = None
        self._ui.diamondScriptRadio.clicked.connect(partial(self.continuous_script_callback, widget=self._ui.diamondScriptRadio))
        self._ui.stoneScriptRadio.clicked.connect(partial(self.continuous_script_callback, widget=self._ui.stoneScriptRadio))

        self._ui.surfaceButton.clicked.connect(partial(self.execute_script_callback, widget=self._ui.surfaceButton))
        self._ui.depthButton.clicked.connect(partial(self.execute_script_callback, widget=self._ui.depthButton))

    def start_agent(self):
        """
        Description:
            Callback function to start the minerl environment process and
            disable the "Start Agent" button until the process ends or joins.
        """
        print("start_agent triggered")
        self._ui.resetEnvironmentButton.setEnabled(True)
        self._ui.agentButton.setEnabled(False)
        self._emitter.start()
        self._backend.start()
        self._emitter.data_available.connect(self.updateUI)

    def updateUI(self):
        data = self._obs_q.get()
        print(data)
        

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
        self._ui.resetEnvironmentButton.setEnabled(True)

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

        # plainFont = QtGui.QFont()
        self._ui.currentObjectiveWidget.setFont(PLAINFONT)
        self._ui.currentObjectiveWidget.setEnabled(True)        # Enable the old objective widget

        self._objective_q.put(newObjective)                     # Update the controller

        self._ui.progressBar.setValue(0)                        # Update the progress bar
        self._ui.currentObjectiveLabel.setText(f"Goal: <b>{newObjective}</b>")
        self._ui.currentObjectiveLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # boldFont = QtGui.QFont()
        # boldFont.setBold(True)
        self._ui.currentObjectiveWidget = widget                # Update current objective widget
        self._ui.currentObjectiveWidget.setFont(BOLDFONT)
        self._ui.currentObjectiveWidget.setEnabled(False)       # Disable current objective widget

    def continuous_script_callback(self, widget):
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
        self._ui.activeScriptWidget.setFont(PLAINFONT)

        self._objective_q.put(script)

        # boldFont = QtGui.QFont()
        # boldFont.setBold(True)
        widget.setFont(BOLDFONT)
        self._ui.activeScriptWidget = widget
        self._ui.stopScriptButton.setEnabled(True)

    def stop_continuous_callback(self):
        """
            Description:
                Callback function that toggles scripts and updates relevant UI elements.
            Inputs:
                widget - The GUI element that triggered the event and should be toggled.
            Output: None
        """
        print("stop_continuous_callback triggered")

        oldObjective = self._ui.currentObjectiveWidget.text().replace('\n', ' ')
        self._objective_q.put(oldObjective)
        self._ui.activeScriptWidget.setFont(PLAINFONT)
        self._ui.activeScriptWidet = None
        self._ui.stopScriptButton.setEnabled(False)

    def execute_script_callback(self, widget):
        """
            Description:
                Callback function that toggles scripts and updates relevant UI elements.
            Inputs:
                widget - The GUI element that triggered the event and should be toggled.
            Output: None
        """
        script = widget.text().replace('\n', ' ')
        print(f"execute_script_callback triggered on {script}")

        # plainFont = QtGui.QFont()
        self._ui.activeScriptWidet.setFont(PLAINFONT)

        self._objective_q.put(script)

        # boldFont = QtGui.QFont()
        # boldFont.setBold(True)
        widget.setFont(BOLDFONT)
        self._ui.activeScriptWidget = widget
        self._ui.stopScriptButton.setEnabled(True)

    def exec(self):
        return self._exit_code