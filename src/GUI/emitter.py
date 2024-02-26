from PyQt6.QtCore import pyqtSignal, QThread
from multiprocessing import Pipe

"""
Emitter code taken and modified from: https://stackoverflow.com/a/72572154
"""

class Emitter(QThread):
    """
    Emitter waits for data from the AgentController and
    emits a signal for the UI to update its appearance.
    """
    data_available = pyqtSignal(str) # Signal indicating new UI data is available.

    def __init__(self, from_process: Pipe):
        super().__init__()
        self.data_from_process = from_process

    def run(self):
        while True:
            try:
                text = self.data_from_process.recv()
            except EOFError:
                break
            else:
                # Pass up the signal type, GUI will check it to
                # decide which queue to check for updates.
                self.data_available.emit(text)