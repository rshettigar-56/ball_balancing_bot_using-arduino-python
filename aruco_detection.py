"""
=========================================================
ArUco Detection + Perspective Transform
=========================================================
"""

import cv2
import numpy as np

from config import *

# ------------------------------------------------------
# ArUco Dictionary
# ------------------------------------------------------

aruco_dict = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_4X4_50
)

parameters = cv2.aruco.DetectorParameters()

detector = cv2.aruco.ArucoDetector(
    aruco_dict,
    parameters
)


class ArucoBoard:

    def __init__(self):

        self.lastHomography = None

        self.markerDict = {}

    # --------------------------------------------------

    def detect(self, frame):

        corners, ids, rejected = detector.detectMarkers(frame)

        self.markerDict.clear()

        if ids is None:

            return False

        ids = ids.flatten()

        for markerCorner, markerID in zip(corners, ids):

            self.markerDict[int(markerID)] = markerCorner

        cv2.aruco.drawDetectedMarkers(
            frame,
            corners,
            ids
        )

        return True

    # --------------------------------------------------

    def hasAllMarkers(self):

        needed = [

            TOP_LEFT,

            TOP_RIGHT,

            BOTTOM_LEFT,

            BOTTOM_RIGHT

        ]

        for m in needed:

            if m not in self.markerDict:

                return False

        return True

    # --------------------------------------------------

    def computeHomography(self):

        tl = self.markerDict[TOP_LEFT][0][0]
        tr = self.markerDict[TOP_RIGHT][0][1]
        br = self.markerDict[BOTTOM_RIGHT][0][2]
        bl = self.markerDict[BOTTOM_LEFT][0][3]
        source = np.array(

            [

                tl,

                tr,

                br,

                bl

            ],

            dtype=np.float32

        )

        destination = np.array(

            [

                [0,0],

                [WARP_SIZE-1,0],

                [WARP_SIZE-1,WARP_SIZE-1],

                [0,WARP_SIZE-1]

            ],

            dtype=np.float32

        )

        self.lastHomography = cv2.getPerspectiveTransform(

            source,

            destination

        )

    # --------------------------------------------------

    def warp(self, frame):

        if self.hasAllMarkers():

            self.computeHomography()

        if self.lastHomography is None:

            return None

        warped = cv2.warpPerspective(

            frame,

            self.lastHomography,

            (

                WARP_SIZE,

                WARP_SIZE

            )

        )

        return warped