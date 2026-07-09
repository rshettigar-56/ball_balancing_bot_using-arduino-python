"""
=========================================================
PID Controller
=========================================================
"""

import time

from config import *

class PID:

    def __init__(self, kp, ki, kd):

        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.integral = 0.0

        self.previousError = 0.0

        self.previousDerivative = 0.0

        self.previousTime = time.time()

    # -------------------------------------------------

    def reset(self):

        self.integral = 0.0

        self.previousError = 0.0

        self.previousDerivative = 0.0

        self.previousTime = time.time()

    # -------------------------------------------------

    def compute(self, error):

        currentTime = time.time()

        dt = currentTime - self.previousTime

        self.previousTime = currentTime

        if dt <= 0:

            dt = 0.001

        # ---------------------------------------
        # Deadband
        # ---------------------------------------

        if abs(error) < DEADBAND:

            error = 0

        # ---------------------------------------
        # Integral
        # ---------------------------------------

        self.integral += error * dt

        if self.integral > INTEGRAL_LIMIT:

            self.integral = INTEGRAL_LIMIT

        elif self.integral < -INTEGRAL_LIMIT:

            self.integral = -INTEGRAL_LIMIT

        # ---------------------------------------
        # Derivative
        # ---------------------------------------

        derivative = (

            error -

            self.previousError

        ) / dt

        # ---------------------------------------
        # Derivative Low-pass Filter
        # ---------------------------------------

        derivative = (

            0.7*self.previousDerivative +

            0.3*derivative

        )

        self.previousDerivative = derivative

        self.previousError = error

        # ---------------------------------------
        # PID Output
        # ---------------------------------------

        output = (

            self.kp*error +

            self.ki*self.integral +

            self.kd*derivative

        )

        # ---------------------------------------
        # Limit Platform Tilt
        # ---------------------------------------

        if output > MAX_TILT:

            output = MAX_TILT

        elif output < -MAX_TILT:

            output = -MAX_TILT

        return output