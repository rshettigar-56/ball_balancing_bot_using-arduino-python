# ball_balancing_bot_using-arduino-python
# 🎯 3-DOF Vision-Based Ball Balancing Robot

A real-time **3-DOF Ball Balancing Robot** developed using **Python, OpenCV, Arduino Uno, and MG996R servo motors**. The system uses computer vision to detect an orange tennis ball, performs perspective correction using ArUco markers, and balances the ball through a closed-loop PID controller and inverse kinematics.

---

## 📷 Project Overview

The robot balances an orange tennis ball on a circular platform by continuously tracking the ball position using a USB camera. The vision and control algorithms can run on a Raspberry Pi 4 Model B or any compatible computer capable of running Python and OpenCV, while an Arduino Uno drives the three servo motors responsible for tilting the platform.

The project evolved through multiple hardware and software iterations, beginning with a square platform using HSV-based detection and later transitioning to a circular platform with ArUco marker-based perspective transformation for improved accuracy.

---

## ✨ Features

- 🎥 Real-time USB camera processing
- 🔲 ArUco marker detection
- 📐 Perspective (Homography) Transformation
- 🟠 HSV-based ball detection
- 📉 Low-pass filtering
- 🎯 Two-axis PID controller
- ⚙️ 3-DOF inverse kinematics
- 🔌 Arduino serial communication
- 🎛 Live PID & HSV tuning using OpenCV Trackbars
- 📊 FPS monitoring and debugging windows

---

## 🛠 Hardware

- USB Camera
- Arduino Uno
- 3 × MG996R Servo Motors
- Circular Top Plate (27 cm Diameter)
- Four ArUco Markers
- Orange Tennis Ball
- External 5V Servo Power Supply

> **Note:** The vision software can be executed on a Raspberry Pi or any computer supporting Python 3 and OpenCV.

---

## 💻 Software

- Python 3
- OpenCV
- NumPy
- PySerial
- Arduino IDE

---

## 📂 Project Structure

```text
3DOF-Ball-Balancing-Robot
│
├── Python
│   ├── main.py
│   ├── config.py
│   ├── camera.py
│   ├── aruco_detection.py
│   ├── ball_detection.py
│   ├── pid_controller.py
│   ├── inverse_kinematics.py
│   ├── serial_comm.py
│   └── tuner.py
│
├── Arduino
│   └── BallBalancer.ino
│
├── Images
│
├── Report
│
└── README.md
```

---

## 🔄 Software Workflow

```text
USB Camera
      │
      ▼
Capture Frame
      │
      ▼
ArUco Detection
      │
      ▼
Perspective Transform
      │
      ▼
Warped Image
      │
      ▼
HSV Ball Detection
      │
      ▼
Low-pass Filter
      │
      ▼
PID Controller
      │
      ▼
Inverse Kinematics
      │
      ▼
Arduino Uno
      │
      ▼
MG996R Servo Motors
      │
      ▼
Platform Tilt
```

---

## 🚀 Getting Started

### Clone the Repository

```bash
git clone https://github.com/USERNAME/3DOF-Ball-Balancing-Robot.git
```

### Install Dependencies

```bash
pip install opencv-python numpy pyserial
```

### Connect

- USB Camera
- Arduino Uno
- External Servo Power Supply

### Run

```bash
python3 main.py
```

---

## 📸 Results

Include:

- Final Robot
- Camera View
- ArUco Detection
- Warped Image
- Ball Detection
- PID Tuning Window

---

## 📈 Future Improvements

- Reinforcement Learning Based Control
- LQR Controller
- Model Predictive Control (MPC)
- Kalman Filtering
- Automatic PID Tuning
- GUI Dashboard
- Multi-ball Tracking

---

## 📚 Documentation

The complete project report, wiring diagrams, and implementation details are available in the **Report** directory.

---

## 👨‍💻 Authors

**Rishit U. Shettigar**  
Department of Electronics & Communication Engineering  
NMAM Institute of Technology

**Aaryaman Ghosh**  
Department of Robotics & Artificial Intelligence  
NMAM Institute of Technology

---

## 🙏 Acknowledgements

We sincerely thank the faculty members, mentors, and the Department of Electronics & Communication Engineering at NMAM Institute of Technology for their continuous guidance and support throughout this project.

---

## 📄 License

This project is intended for educational, research, and learning purposes.
