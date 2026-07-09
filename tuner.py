"""
=========================================================
Live Robot Tuner
3 DOF Ball Balancer
=========================================================
"""

import cv2

from config import *


class LiveTuner:

    def __init__(self):

        cv2.namedWindow("Robot Tuning", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Robot Tuning", 500, 750)

        # -------------------------------------------------
        # PID
        # -------------------------------------------------

        cv2.createTrackbar(
            "KP x1000",
            "Robot Tuning",
            int(KP * 1000),
            500,
            lambda x: None
        )

        cv2.createTrackbar(
            "KI x1000",
            "Robot Tuning",
            int(KI * 1000),
            100,
            lambda x: None
        )

        cv2.createTrackbar(
            "KD x1000",
            "Robot Tuning",
            int(KD * 1000),
            500,
            lambda x: None
        )

        # -------------------------------------------------
        # Filtering
        # -------------------------------------------------

        cv2.createTrackbar(
            "Alpha x100",
            "Robot Tuning",
            int(ALPHA * 100),
            100,
            lambda x: None
        )

        # -------------------------------------------------
        # Platform
        # -------------------------------------------------

        cv2.createTrackbar(
            "Servo Gain x10",
            "Robot Tuning",
            int(SERVO_GAIN * 10),
            50,
            lambda x: None
        )

        cv2.createTrackbar(
            "Max Tilt",
            "Robot Tuning",
            MAX_TILT,
            30,
            lambda x: None
        )

        cv2.createTrackbar(
            "Max Command x10",
            "Robot Tuning",
            30,
            100,
            lambda x: None
        )

        # -------------------------------------------------
        # Servo
        # -------------------------------------------------

        cv2.createTrackbar(
            "Servo Center",
            "Robot Tuning",
            SERVO_CENTER,
            180,
            lambda x: None
        )

        cv2.createTrackbar(
            "Offset1",
            "Robot Tuning",
            SERVO1_OFFSET + 50,
            100,
            lambda x: None
        )

        cv2.createTrackbar(
            "Offset2",
            "Robot Tuning",
            SERVO2_OFFSET + 50,
            100,
            lambda x: None
        )

        cv2.createTrackbar(
            "Offset3",
            "Robot Tuning",
            SERVO3_OFFSET + 50,
            100,
            lambda x: None
        )

        # -------------------------------------------------
        # HSV
        # -------------------------------------------------

        cv2.createTrackbar(
            "H Min",
            "Robot Tuning",
            HSV_LOWER[0],
            179,
            lambda x: None
        )

        cv2.createTrackbar(
            "H Max",
            "Robot Tuning",
            HSV_UPPER[0],
            179,
            lambda x: None
        )

        cv2.createTrackbar(
            "S Min",
            "Robot Tuning",
            HSV_LOWER[1],
            255,
            lambda x: None
        )

        cv2.createTrackbar(
            "S Max",
            "Robot Tuning",
            HSV_UPPER[1],
            255,
            lambda x: None
        )

        cv2.createTrackbar(
            "V Min",
            "Robot Tuning",
            HSV_LOWER[2],
            255,
            lambda x: None
        )

        cv2.createTrackbar(
            "V Max",
            "Robot Tuning",
            HSV_UPPER[2],
            255,
            lambda x: None
        )

        cv2.createTrackbar(
            "Min Area",
            "Robot Tuning",
            MIN_BALL_AREA,
            3000,
            lambda x: None
        )

    # =====================================================

    def update(self):

        values = {}

        # PID

        values["kp"] = cv2.getTrackbarPos(
            "KP x1000",
            "Robot Tuning"
        ) / 1000.0

        values["ki"] = cv2.getTrackbarPos(
            "KI x1000",
            "Robot Tuning"
        ) / 1000.0

        values["kd"] = cv2.getTrackbarPos(
            "KD x1000",
            "Robot Tuning"
        ) / 1000.0

        # Filtering

        values["alpha"] = cv2.getTrackbarPos(
            "Alpha x100",
            "Robot Tuning"
        ) / 100.0

        # Platform

        values["servo_gain"] = cv2.getTrackbarPos(
            "Servo Gain x10",
            "Robot Tuning"
        ) / 10.0

        values["max_tilt"] = cv2.getTrackbarPos(
            "Max Tilt",
            "Robot Tuning"
        )

        values["max_command"] = cv2.getTrackbarPos(
            "Max Command x10",
            "Robot Tuning"
        ) / 10.0

        # Servo

        values["servo_center"] = cv2.getTrackbarPos(
            "Servo Center",
            "Robot Tuning"
        )

        values["offset1"] = (
            cv2.getTrackbarPos(
                "Offset1",
                "Robot Tuning"
            ) - 50
        )

        values["offset2"] = (
            cv2.getTrackbarPos(
                "Offset2",
                "Robot Tuning"
            ) - 50
        )

        values["offset3"] = (
            cv2.getTrackbarPos(
                "Offset3",
                "Robot Tuning"
            ) - 50
        )

        # HSV

        values["hmin"] = cv2.getTrackbarPos(
            "H Min",
            "Robot Tuning"
        )

        values["hmax"] = cv2.getTrackbarPos(
            "H Max",
            "Robot Tuning"
        )

        values["smin"] = cv2.getTrackbarPos(
            "S Min",
            "Robot Tuning"
        )

        values["smax"] = cv2.getTrackbarPos(
            "S Max",
            "Robot Tuning"
        )

        values["vmin"] = cv2.getTrackbarPos(
            "V Min",
            "Robot Tuning"
        )

        values["vmax"] = cv2.getTrackbarPos(
            "V Max",
            "Robot Tuning"
        )

        values["min_ball_area"] = cv2.getTrackbarPos(
            "Min Area",
            "Robot Tuning"
        )

        return values