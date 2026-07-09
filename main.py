"""
=========================================================
MAIN PROGRAM
3 DOF Ball Balancing Robot

Raspberry Pi 4
Pi Camera V2
Arduino UNO

=========================================================
"""

import cv2

from config import *

from camera import Camera
from aruco_detection import ArucoBoard
from ball_detection import BallDetector
from pid_controller import PID
from inverse_kinematics import inverse_kinematics
from serial_comm import Arduino
from tuner import LiveTuner
# ==========================================================
# INITIALIZE
# ==========================================================

print("Starting Ball Balancer...")

camera = Camera()

board = ArucoBoard()

ball = BallDetector()

arduino = Arduino()
tuner= LiveTuner()

pidX = PID(KP, KI, KD)
pidY = PID(KP, KI, KD)

print("System Ready")

# ==========================================================
# MAIN LOOP
# ==========================================================

while True:
    values = tuner.update()
    # -----------------------------------------
    # Capture Camera Frame
    # -----------------------------------------

    frame = camera.read()
    
    if frame is None:
        continue

    displayFrame = frame.copy()

    # -----------------------------------------
    # Detect ArUco Markers
    # -----------------------------------------

    detected = board.detect(displayFrame)

    # No markers at all

    if not detected:

        arduino.center()

        if SHOW_CAMERA:

            cv2.putText(

                displayFrame,

                "Searching for ArUco Markers",

                (20,40),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.8,

                (0,0,255),

                2

            )

            cv2.imshow(

                "Camera",

                displayFrame

            )

        if cv2.waitKey(1) & 0xFF == ord('q'):

            break

        continue

    # -----------------------------------------
    # Warp Board
    # -----------------------------------------

    warped = board.warp(frame)

    if warped is None:

        arduino.center()

        if SHOW_CAMERA:

            cv2.imshow(

                "Camera",

                displayFrame

            )

        if cv2.waitKey(1) & 0xFF == ord('q'):

            break

        continue

    # -----------------------------------------
    # Ball Detection
    # -----------------------------------------

    result, mask = ball.detect(

        warped

    )

    # -----------------------------------------
    # Ball Lost
    # -----------------------------------------

    if result is None:

        pidX.reset()

        pidY.reset()

        arduino.center()

        cv2.putText(

            warped,

            "BALL LOST",

            (210,40),

            cv2.FONT_HERSHEY_SIMPLEX,

            1,

            (0,0,255),

            2

        )

        if SHOW_CAMERA:

            cv2.imshow(

                "Camera",

                displayFrame

            )

        if SHOW_WARP:

            cv2.imshow(

                "Warped",

                warped

            )

        if SHOW_MASK:

            cv2.imshow(

                "Mask",

                mask

            )

        if cv2.waitKey(1) & 0xFF == ord('q'):

            break

        continue

    # -----------------------------------------
    # Draw Ball
    # -----------------------------------------

    warped = ball.draw(

        warped,

        result

    )

    # -----------------------------------------
    # Error Calculation
    # -----------------------------------------

    errors = ball.getError(result)

    if errors is None:

        continue

    errorX, errorY = errors

    # -----------------------------------------
    # PID
    # -----------------------------------------
    pidX.kp = values["kp"]
    pidX.ki = values["ki"]
    pidX.kd = values["kd"]

    pidY.kp = values["kp"]
    pidY.ki = values["ki"]
    pidY.kd = values["kd"]

    roll = pidX.compute(errorX)
    pitch = pidY.compute(errorY)
    
    MAX_COMMAND = values["max_command"]

    roll = max(-MAX_COMMAND, min(MAX_COMMAND, roll))
    pitch = max(-MAX_COMMAND, min(MAX_COMMAND, pitch))
# -----------------------------------------
    # Inverse Kinematics
    # -----------------------------------------

    theta1, theta2, theta3 = inverse_kinematics(
        roll,
        pitch,
        values["servo_gain"],
        values["servo_center"],
        values["offset1"],
        values["offset2"],
        values["offset3"]
    )

    print(f"Roll={roll:.2f}, Pitch={pitch:.2f}")
    print(f"Theta1={theta1}, Theta2={theta2}, Theta3={theta3}")
    # -----------------------------------------
    # Send Servo Angles
    # -----------------------------------------

    arduino.send(
        theta1,
        theta2,
        theta3
    )

    # -----------------------------------------
    # Debug Information
    # -----------------------------------------

    if SHOW_DEBUG:

        x, y, fx, fy, radius = result

        cv2.putText(
            warped,
            f"Ball : ({x},{y})",
            (10,25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0,255,0),
            2
        )

        cv2.putText(
            warped,
            f"Filtered : ({fx},{fy})",
            (10,50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255,0,255),
            2
        )

        cv2.putText(
            warped,
            f"Error X : {errorX:.1f}",
            (10,80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255,255,0),
            2
        )

        cv2.putText(
            warped,
            f"Error Y : {errorY:.1f}",
            (10,105),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255,255,0),
            2
        )

        cv2.putText(
            warped,
            f"Roll : {roll:.2f}",
            (10,135),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255,0,0),
            2
        )

        cv2.putText(
            warped,
            f"Pitch : {pitch:.2f}",
            (10,160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255,0,0),
            2
        )

        cv2.putText(
            warped,
            f"S1 : {theta1}",
            (10,190),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0,255,255),
            2
        )

        cv2.putText(
            warped,
            f"S2 : {theta2}",
            (10,215),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0,255,255),
            2
        )

        cv2.putText(
            warped,
            f"S3 : {theta3}",
            (10,240),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0,255,255),
            2
        )

        cv2.putText(
            warped,
            f"FPS : {camera.getFPS():.1f}",
            (10,270),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0,255,0),
            2

        )

    # -----------------------------------------
    # Display Windows
    # -----------------------------------------
  
    if SHOW_CAMERA:
        
        cv2.putText(
            frame,
            f"FPS: {camera.getFPS():.1f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )
        cv2.imshow(
            "Camera",
            displayFrame
        )

    if SHOW_WARP:

        cv2.imshow(
            "Warped",
            warped
        )

    if SHOW_MASK:

        cv2.imshow(
            "Mask",
            mask
        )

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):

        break

# ==========================================================
# Cleanup
# ==========================================================

print("Stopping...")

arduino.center()

arduino.close()

camera.stop()

cv2.destroyAllWindows()

print("Program Closed")