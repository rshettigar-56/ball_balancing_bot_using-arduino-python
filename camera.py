"""
=========================================================
USB Camera Module
=========================================================
"""

import cv2
import time

from config import *

class Camera:

    def __init__(self):

        self.cap = cv2.VideoCapture(1)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        print(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        print(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Optional: reduce internal buffering to reduce latency
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        if not self.cap.isOpened():
            raise RuntimeError("Cannot open USB Camera (/dev/video0)")

        self.frameCounter = 0
        self.lastTime = time.time()
        self.fps = 0

        print("USB Camera Ready")

    def read(self):

        ret, frame = self.cap.read()

        if not ret:
            return None

        self.frameCounter += 1

        currentTime = time.time()

        elapsed = currentTime - self.lastTime

        if elapsed >= 1:

            self.fps = self.frameCounter / elapsed

            self.frameCounter = 0
            self.lastTime = currentTime

        return frame

    def getFPS(self):

        return self.fps

    def stop(self):

        self.cap.release()