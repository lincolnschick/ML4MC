import pyautogui
import cv2
import numpy as np
from multiprocessing import Queue
from datetime import datetime
import os

from backend import Message

class ScreenRecorder:
    def __init__(self, dirname: str, record_q: Queue):
        self._record_q = record_q
        size = pyautogui.size()

        # Required for cv2.VideoWriter
        self._resolution = (size.width, size.height)
        self._fps = 60.0
        self._fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self._dirname = dirname
        self._path = self._dirname + os.path.sep + "recordings" + os.path.sep

    def run(self):
        while True:
            msg = None
            while not self._record_q.empty():
                # Consume all messages in Queue
                msg = self._record_q.get()

            # Check final message received
            if msg == Message.QUIT:
                # End loop to kill process and join.
                break
            elif msg == Message.START_RECORDING:
                # Create directory for recordings if they don't already exist
                os.makedirs(self._dirname + os.path.sep + "recordings", exist_ok=True)
                time = str(datetime.now())      # Use current time for unique file names
                time = time[0:time.find(".")].replace(" ", "_").replace(":", "-")   # Clean up time to shorten and sanitize for file system
                filename = self._path + "ML4MC_" + time + ".avi"
                out = cv2.VideoWriter(filename, self._fourcc, self._fps, self._resolution)

                # Record until we get a new signal in the queue (that signal can only be QUIT or STOP)
                while self._record_q.empty():
                    img = pyautogui.screenshot()

                    frame = np.array(img)

                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    out.write(frame)
                    
                # Clean up
                out.release()
                cv2.destroyAllWindows()
                if self._record_q.get() == Message.QUIT:
                    # End loop to kill process and join.
                    break

        

