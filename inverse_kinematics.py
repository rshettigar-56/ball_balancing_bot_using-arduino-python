"""
====================================================
Inverse Kinematics
3 DOF Ball Balancer
====================================================
"""

import math
from config import *

# ----------------------------------------------------
# Top Plate Joint Radius (Measured)
# ----------------------------------------------------

R1 = 110.0
R2 = 115.0
R3 = 100.0

# ----------------------------------------------------
# Joint Angles
#
#           J1
#
#
#    J2            J3
#
# ----------------------------------------------------

A1 = math.radians(90)
A2 = math.radians(210)
A3 = math.radians(330)

# ----------------------------------------------------

SERVO_ARM = 70.26

# ----------------------------------------------------

B1 = (
    R1 * math.cos(A1),
    R1 * math.sin(A1)
)

B2 = (
    R2 * math.cos(A2),
    R2 * math.sin(A2)
)

B3 = (
    R3 * math.cos(A3),
    R3 * math.sin(A3)
)

# ----------------------------------------------------

def inverse_kinematics(
    roll,
    pitch,
    servo_gain=SERVO_GAIN,
    servo_center=SERVO_CENTER,
    offset1=SERVO1_OFFSET,
    offset2=SERVO2_OFFSET,
    offset3=SERVO3_OFFSET,
):

    # Joint 1
    theta1 = servo_center +  servo_gain * (
        (B1[0] / SERVO_ARM) * pitch
        -
        (B1[1] / SERVO_ARM) * roll
    )

    # Joint 2
    theta2 = servo_center - servo_gain * (
        (B2[0] / SERVO_ARM) * pitch
        -
        (B2[1] / SERVO_ARM) * roll
    )

    # Joint 3
    theta3 = servo_center +  servo_gain * (
        (B3[0] / SERVO_ARM) * pitch
        -
        (B3[1] / SERVO_ARM) * roll
    )

    # Servo offsets
    theta1 += offset1
    theta2 += offset2
    theta3 += offset3

    # Servo limits
    theta1 = max(SERVO_MIN, min(SERVO_MAX, theta1))
    theta2 = max(SERVO_MIN, min(SERVO_MAX, theta2))
    theta3 = max(SERVO_MIN, min(SERVO_MAX, theta3))

    return (
        int(theta1),
        int(theta2),
        int(theta3)
    )