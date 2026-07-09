"""
=========================================================
Ball Detection Module
=========================================================
"""

import cv2
import numpy as np

from config import *

class BallDetector:

    def __init__(self):

        self.filteredX = BOARD_CENTER_X
        self.filteredY = BOARD_CENTER_Y

    # -------------------------------------------------

    def detect(self, warped):

        hsv = cv2.cvtColor(
            warped,
            cv2.COLOR_BGR2HSV
        )

        mask = cv2.inRange(
            hsv,
            HSV_LOWER,
            HSV_UPPER
        )

        mask = cv2.GaussianBlur(
            mask,
            (5,5),
            0
        )

        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_OPEN,
            KERNEL
        )

        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_CLOSE,
            KERNEL
        )

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if len(contours) == 0:

            return None, mask

        contour = max(
            contours,
            key=cv2.contourArea
        )

        area = cv2.contourArea(contour)

        if area < MIN_BALL_AREA:

            return None, mask

        (x,y),radius = cv2.minEnclosingCircle(
            contour
        )

        x = int(x)
        y = int(y)
        radius = int(radius)

        # -----------------------------------

        self.filteredX = (

            ALPHA*x +

            (1-ALPHA)*self.filteredX

        )

        self.filteredY = (

            ALPHA*y +

            (1-ALPHA)*self.filteredY

        )

        return (

            x,
            y,

            int(self.filteredX),

            int(self.filteredY),

            radius

        ), mask

    # -------------------------------------------------

    def draw(self, frame, result):

        if result is None:

            return frame

        x,y,fx,fy,radius = result

        cv2.circle(

            frame,

            (x,y),

            radius,

            (0,255,0),

            2

        )

        cv2.circle(

            frame,

            (x,y),

            5,

            (0,0,255),

            -1

        )

        cv2.circle(

            frame,

            (fx,fy),

            5,

            (255,0,255),

            -1

        )

        cv2.circle(

            frame,

            (

                BOARD_CENTER_X,

                BOARD_CENTER_Y

            ),

            6,

            (255,255,0),

            2

        )

        cv2.line(

            frame,

            (BOARD_CENTER_X,0),

            (BOARD_CENTER_X,WARP_SIZE),

            (255,255,0),

            1

        )

        cv2.line(

            frame,

            (0,BOARD_CENTER_Y),

            (WARP_SIZE,BOARD_CENTER_Y),

            (255,255,0),

            1

        )

        return frame

    # -------------------------------------------------

    def getError(self,result):

        if result is None:

            return None

        _,_,fx,fy,_ = result

        errorX = BOARD_CENTER_X - fx

        errorY = BOARD_CENTER_Y - fy

        if abs(errorX) < DEADBAND:

            errorX = 0

        if abs(errorY) < DEADBAND:

            errorY = 0

        return errorX,errorY