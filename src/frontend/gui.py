from PyQt6 import QtCore, QtGui, QtWidgets
from multiprocessing import Process, Queue
from functools import partial
import re

from frontend.generated import Ui_MainWindow
from backend import Emitter, Script, Objective, Message

PLAINFONT = QtGui.QFont()
BOLDFONT = QtGui.QFont()
BOLDFONT.setBold(True)
STRIKEFONT = QtGui.QFont()
STRIKEFONT.setStrikeOut(True)

class GUI():
    def __init__(
            self,
            args,
            backend_ai: Process,
            recorder: Process,
            emitter: Emitter, 
            obs_q: Queue, 
            objective_q: Queue, 
            restart_q: Queue, 
            quit_q: Queue,
            pause_q: Queue,
            pov_q: Queue,
            interactor_q: Queue,
            record_q: Queue
        ):
        """
        GUI object to represent and manage the PyQt6 GUI, apply functionality to
        widgets, and utilize queues to send messages and updates to backend processes.

        Inputs / Member Variables:
            backend_ai: The process running the AgentController
            recorder: The process running the ScreenRecorder
            emitter: The Emitter object running on another thread,
                     passes messages from backend to the GUI
            obs_q: The queue handling observation data from the backend
            objective_q: The queue handling objective update messages
            restart_q: The queue handling restart signals
            quit_q: The queue handling signals to quit the application.
            pause_q: The queue handling signals to pause Agent actions.
            pov_q: The queue handling signals to toggle displaying the Agent's POV
            interactor_q: The queue 
        """
        self._backend_ai = backend_ai
        self._recorder = recorder
        self._emitter = emitter
        self._obs_q = obs_q
        self._objective_q = objective_q
        self._restart_q = restart_q
        self._quit_q = quit_q
        self._pause_q = pause_q
        self._pov_q = pov_q
        self._interactor_q = interactor_q
        self._record_q = record_q
        
        self._app = QtWidgets.QApplication(args)
        self._app.setStyle("Fusion")
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

        # Objective Controls
        self.currentObjectiveWidget = self._ui.woodRadio
        self._ui.woodRadio.clicked.connect(partial(self.objective_clicked, widget=self._ui.woodRadio))
        self._ui.stoneRadio.clicked.connect(partial(self.objective_clicked, widget=self._ui.stoneRadio))
        self._ui.ironRadio.clicked.connect(partial(self.objective_clicked, widget=self._ui.ironRadio))
        self._ui.combatRadio.clicked.connect(partial(self.objective_clicked, widget=self._ui.combatRadio))

        # Interactor / Agent POV Loading Controls
        self._ui.agentCheckbox.clicked.connect(self.toggle_agent_pov)
        self._ui.interactorCheckbox.clicked.connect(self.toggle_interactor)

        # Agent Pause/Play Controls
        self._ui.playButton.mousePressEvent = self.play_agent
        self._ui.pauseButton.mousePressEvent = self.pause_agent

        # Recording Controls
        self._ui.recordButton.mousePressEvent = self.start_recording
        self._ui.stopButton.mousePressEvent = self.stop_recording

        # Setup Inventory Table
        self.inventory: list = []
        self._ui.inventoryTable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        header = self._ui.inventoryTable.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        
        # Scripts Controls
        self.activeScriptWidget: QtWidgets.QPushButton = None
        self.currentScript: Script = None
        self._ui.stopScriptButton.clicked.connect(self.stop_script)
            # Continuous Scripts
        self._ui.diamondScriptButton.clicked.connect(partial(self.start_script, widget=self._ui.diamondScriptButton))
        self._ui.stoneScriptButton.clicked.connect(partial(self.start_script, widget=self._ui.stoneScriptButton))
            # Execute Once Scripts
        self._ui.surfaceScriptButton.clicked.connect(partial(self.start_script, widget=self._ui.surfaceScriptButton))
        self._ui.pickaxeScriptButton.clicked.connect(partial(self.start_script, widget=self._ui.pickaxeScriptButton))
        self._ui.swordScriptButton.clicked.connect(partial(self.start_script, widget=self._ui.swordScriptButton))

    # Process / Thread Communication Functions
    def handle_notification(self, msg: Message):
        """
        Description:
            Callback function to read the Message sent by the emitter
            and call the appropriate function for the GUI.
        """
        print("handle_notification triggered")
        if msg == Message.RESTART_FINISHED:
            self.restart_finished()
        elif msg == Message.SCRIPT_FINISHED:
            self.script_finished()

    # Agent / Environment Functions
    def start_agent(self):
        """
        Description:
            Callback function to start the minerl environment process and
            disable the "Start Agent" button until the process ends or joins.
            Also enables controls that are availabe once agent has started.
        """
        print("start_agent triggered")
        # Enable Restart Button
        self._ui.resetEnvironmentButton.setEnabled(True)
        # Continuous Scripts
        self._ui.diamondScriptButton.setEnabled(True)
        self._ui.stoneScriptButton.setEnabled(True)
        # Single Execution Scripts
        self._ui.surfaceScriptButton.setEnabled(True)
        self._ui.pickaxeScriptButton.setEnabled(True)
        self._ui.swordScriptButton.setEnabled(True)
        # Agent Controls
        self._ui.agentButton.setEnabled(False)
        self._ui.pauseButton.setEnabled(True)
        # Recording Controls
        self._ui.recordButton.setEnabled(True)
        # Backend Processes
        self._emitter.start()
        self._backend_ai.start()
        self._recorder.start()
        # Connect Emitter Signals
        self._emitter.data_available.connect(self.update_statistics)
        self._emitter.notification.connect(self.handle_notification)

    def reload_environment_callback(self):
        """
            Description:
                Function to reload the custom ML4MC
                environment after user input via GUI.
        """
        print("reload_environment triggered")
        self._ui.resetEnvironmentButton.setEnabled(False)
        self._ui.pauseButton.setEnabled(False)
        self._ui.recordButton.setEnabled(False)

        # Reset the inventory to be empty
        self.inventory = []
        
        # Send message to controller to restart the environment
        self._restart_q.put(Message.RESTART)

    def restart_finished(self):
        """
        Description:
            Function to enable the Restart Environment button
            once given the signal it is safe to do so.
        """
        print("enable_restart triggered")
        self._ui.resetEnvironmentButton.setEnabled(True)
        self._ui.pauseButton.setEnabled(True)
        self._ui.recordButton.setEnabled(True)

    def widget_to_objective(self, widget: QtWidgets.QRadioButton) -> Message:
        """
        Description:
            Take in a QtWidget RadioButton and convert
            it to the corresponding Objective flag.
        """
        match widget:
            case self._ui.ironRadio:
                return Objective.IRON
            case self._ui.stoneRadio:
                return Objective.STONE
            case self._ui.woodRadio:
                return Objective.WOOD
            case self._ui.combatRadio:
                return Objective.ENEMIES
            case _:
                raise RuntimeError(f"Invalid widget for objective conversion: {widget.objectName()}")

    def objective_clicked(self, widget: QtWidgets.QRadioButton):
        """
            Description:
                Callback function that updates the selected
                AI objective and relevant UI elements.
            Inputs:
                widget - The GUI element (QRadioButton) that triggered the event.
            Output: None
        """
        print(f"objective_clicked triggered on {widget.objectName()}")
        msg = self.widget_to_objective(widget)

        # Restore text and disable stop script button if a script was running
        if self.currentScript != None:
            self.restore_script_text()
            self._ui.stopScriptButton.setEnabled(False)

        # Restore old objective widget text to normal and enable
        self.currentObjectiveWidget.setFont(PLAINFONT)
        self.currentObjectiveWidget.setEnabled(True)

        self._objective_q.put(msg)     # Update the controller

        # Update the goal text
        goalText = widget.text().strip()
        self._ui.currentObjectiveLabel.setText(f"Goal: <b>{goalText}</b>")
        self._ui.currentObjectiveLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Update current object widget tracker and disable
        self.currentObjectiveWidget = widget
        self.currentObjectiveWidget.setFont(BOLDFONT)
        self.currentObjectiveWidget.setEnabled(False)

    def toggle_agent_pov(self):
        """
        Description:
            Sends a signal on whether or not to
            load the Agent POV on start / restart.
        """
        print("toggle_agent_pov triggered")
        self._pov_q.put(self._ui.agentCheckbox.isChecked())

    def toggle_interactor(self):
        """
        Description:
            Sends a signal on whether or not to
            load the Interactor on start / restart.
        """
        print("toggle_interactor_pov triggered")
        self._interactor_q.put(self._ui.interactorCheckbox.isChecked())

    # Statistics Functions
    def update_statistics(self, obs):
        """
        Description:
            Function to update the GUI's display of the agent's statistics,
            including inventory, life, food, x_pos, y_pos, and z_pos.
        Inputs:
            obs: The list of current observations sent from the backend
        """
        self._ui.xCoordLabel.setText("X: " + str(int(obs['location_stats']['xpos'])))
        self._ui.yCoordLabel.setText("Y: " + str(int(obs['location_stats']['ypos'])))
        self._ui.zCoordLabel.setText("Z: " + str(int(obs['location_stats']['zpos'])))
        self._ui.healthLabel.setText(str(obs['life_stats']['life']))
        self._ui.hungerLabel.setText(str(obs['life_stats']['food']))

        # Grab inventory items with non-zero counts
        new_inventory = [(item, count) for item, count in obs['inventory'].items() if count != 0 and item != 'air']
        if new_inventory != self.inventory:
            if len(new_inventory) != len(self.inventory): # If the inventory has changed size, resize the table
                self._ui.inventoryTable.setRowCount(len(new_inventory))

            new_inventory.sort(key=lambda x: -x[1]) # Sort by count in descending order
            for i, (item, count) in enumerate(new_inventory):
                countItem = QtWidgets.QTableWidgetItem(str(count))
                countItem.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self._ui.inventoryTable.setItem(i, 0, QtWidgets.QTableWidgetItem(item))
                self._ui.inventoryTable.setItem(i, 1, countItem)

            self.inventory = new_inventory # Update the inventory for future comparisons

    # Agent Pause / Play Functions
    def pause_agent(self, _):
        """
            Description:
                Callback function to send the pause signal to the controller,
                enable the play button, and disable the pause button.
            Inputs:
                _ - Any, all are disregarded.
        """
        self._pause_q.put(Message.PAUSE_AGENT)
        self._ui.playButton.setEnabled(True)
        self._ui.pauseButton.setEnabled(False)

    def play_agent(self, _):
        """
            Description:
                Callback function to send the play signal to the controller,
                enable the pause button, and disable the play button.
            Inputs:
                _ - Any, all are disregarded.
        """
        self._pause_q.put(Message.PLAY_AGENT)
        self._ui.playButton.setEnabled(False)
        self._ui.pauseButton.setEnabled(True)

    # Recording Functions
    def start_recording(self, _):
        """
        Description:
            Places a flag to start recording on the recording queue.
        Inputs:
            _ - Any, all are disregarded.
        """
        self._ui.recordButton.setEnabled(False)
        self._ui.stopButton.setEnabled(True)
        self._record_q.put(Message.START_RECORDING)
    
    def stop_recording(self, _):
        """
        Description:
            Places a flag to stop recording
            on the recording queue.
        Inputs:
            _ - Any, all are disregarded.
        """
        self._ui.recordButton.setEnabled(True)
        self._ui.stopButton.setEnabled(False)
        self._record_q.put(Message.STOP_RECORDING)

    # Script Functions
    def start_script(self, widget: QtWidgets.QPushButton):
        """
            Description:
                Callback function that sets the triggering
                scripts as the current task for the agent.
            Inputs:
                widget - The GUI element (QPushButton) that triggered the event.
        """
        print(f"start_script triggered on {widget.objectName()}")
        match widget:
            case self._ui.diamondScriptButton:
                script = Script.DIAMOND
            case self._ui.stoneScriptButton:
                script = Script.STONE
            case self._ui.surfaceScriptButton:
                script = Script.SURFACE
            case self._ui.pickaxeScriptButton:
                script = Script.PICKAXE
            case self._ui.swordScriptButton:
                script = Script.SWORD

        if self.activeScriptWidget != None:
            self.restore_script_text()

        self._objective_q.put(script)

        self.activeScriptWidget = widget
        self.activeScriptText = widget.text()
        widget.setFont(BOLDFONT)
        widget.setText("Running...")
        self.activeScriptWidget.setEnabled(False)
        self._ui.stopScriptButton.setEnabled(True)

    def stop_script(self):
        """
            Description:
                Callback function that stops the currently running script
                and restores the previously selected objective.
        """
        print("stop_script triggered")
        oldObj = self.widget_to_objective(self.currentObjectiveWidget)
        self._objective_q.put(oldObj)
        self.restore_script_text()
        self.activeScriptWidget = None
        self.activeScriptText = ""
        self._ui.stopScriptButton.setEnabled(False)

    def script_finished(self):
        """
        Description:
            Function to restore the completed script's text
            and restore the previously running objective.
        """
        print("script_finished triggered")
        self.restore_script_text()
        oldObj = self.widget_to_objective(self.currentObjectiveWidget)
        self._objective_q.put(oldObj)
        self._ui.stopScriptButton.setEnabled(False)
        self.activeScriptWidget = None
        self.activeScriptText = ""

    def restore_script_text(self):
        """
        Description:
            Restore the previously activated script's
            text to its original state.
        """
        self.activeScriptWidget.setFont(PLAINFONT)
        self.activeScriptWidget.setText(self.activeScriptText)
        self.activeScriptWidget.setEnabled(True)

    def clean_objective_string(self, objective):
        """
        Description:
            Function to clean the objective string
            before sending it to the controller.

        NO LONGER USED SINCE WE JUST PASS Message (Enum). Keeping around just incase
        """
        # Remove extra spaces and newlines
        return re.sub(' +', ' ', objective.replace('\n', ' ').strip())

    def exec(self):
        return self._exit_code