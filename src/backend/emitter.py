from PyQt6.QtCore import pyqtSignal, QThread
from multiprocessing import Queue
from time import sleep

from backend import Message

"""
Emitter code taken and modified from: https://stackoverflow.com/a/72572154
"""

class Emitter(QThread):
    """
    Description:
        Emitter waits for data from the AgentController and
        emits a signal for the UI to update its appearance.
    """
    data_available = pyqtSignal(dict) # Signal indicating new UI data is available.
    notification = pyqtSignal(Message) # Signal notifying the UI to make a change.

    def __init__(self, obs_q: Queue, notify_q: Queue):
        super().__init__()
        self.obs_q = obs_q
        self.notify_q = notify_q

    def run(self):
        """
        Description:
            Process loop to keep checking
            observation and notification queues
        """
        while True:
            sleep(0.1)
            if not self.obs_q.empty(): # There will only be one observation at a time
                obs = self.obs_q.get()
                # Pass up the signal type, GUI will check it to
                # decide which queue to check for updates.
                self.data_available.emit(obs)
            
            while not self.notify_q.empty(): # There may be multiple notifications, send them all
                notification = self.notify_q.get()
                self.notification.emit(notification)