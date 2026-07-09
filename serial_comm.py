"""
=========================================================
Serial Communication
Raspberry Pi -> Arduino
=========================================================
"""

import serial
import time

from config import *

class Arduino:

    def __init__(self):

        self.connected = False

        self.previousAngles = (
            SERVO_CENTER,
            SERVO_CENTER,
            SERVO_CENTER
        )

        try:

            self.serial = serial.Serial(
                SERIAL_PORT,
                BAUDRATE,
                timeout=1
            )

            time.sleep(2)

            self.connected = True

            print("Arduino Connected")

            # Move platform to center
            self.send(
                SERVO_CENTER,
                SERVO_CENTER,
                SERVO_CENTER
            )

        except Exception as e:

            print("Arduino Connection Failed")
            print(e)

            self.connected = False

    # ---------------------------------------------------

    def send(self, theta1, theta2, theta3):

        if not self.connected:
            return

        theta1 = int(theta1)
        theta2 = int(theta2)
        theta3 = int(theta3)

        currentAngles = (
            theta1,
            theta2,
            theta3
        )

        # Avoid sending duplicate values
        if currentAngles == self.previousAngles:
            return

        self.previousAngles = currentAngles

        message = f"{theta1},{theta2},{theta3}\n"
      

        try:

            self.serial.write(
                message.encode()
            )

        except Exception:

            self.connected = False

            print("Serial Write Failed")

    # ---------------------------------------------------

    def center(self):

        self.send(
            SERVO_CENTER,
            SERVO_CENTER,
            SERVO_CENTER
        )

    # ---------------------------------------------------

    def close(self):

        if self.connected:

            self.center()

            time.sleep(0.2)

            self.serial.close()

            print("Arduino Closed")