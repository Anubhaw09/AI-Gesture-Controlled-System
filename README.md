AI Gesture-Controlled System

Volume 🔊 | Brightness 💡 | Media 🎵 Control using Hand Gestures



📌 Overview

This project is a real-time gesture control system that allows you to control your computer using hand gestures captured via webcam.

Instead of using a mouse or keyboard, you can:

Adjust volume

Control screen brightness

Play/Pause music

Skip tracks


👉 All using simple hand gestures!


🚀 Features
✋ Real-time hand tracking using MediaPipe

🔊 Volume control (finger distance)

💡 Brightness control (gesture-based)

🎵 Media controls:
      Play / Pause
      Next Track
      Previous Track

🧠 Rule-based gesture recognition (fast & efficient)

🖥️ On-screen gesture labels (UI feedback)

⚡ Smooth and stable performance


🛠️ Technologies Used
    Python 3.10
    OpenCV
    MediaPipe
    NumPy
    PyAutoGUI
    PyCAW (for volume control)
    Screen Brightness Control


    
📂 Project Structure


gesture-control/

│

├── gesture_recognition.py   # Main program

└──README.md                # Project documentation




⚙️ Installation


1️⃣ Install Python
Use Python 3.10 (recommended)

2️⃣ Install Required Libraries
pip install opencv-python mediapipe numpy pyautogui pycaw comtypes screen-brightness-control

3️⃣ Run the Project
python gesture_recognition.py

✋ Gesture Controls
Gesture	Action

🤏 Thumb + Index Distance	Volume Control

🤏 Thumb + Middle Distance	Brightness Control

✊ Closed Fist	Mute + Pause

✋ Open Hand	Play

👉 Index Finger Up	Next Track

👍 Thumb Up	Previous Track


🧠 How It Works


Webcam captures live video

MediaPipe detects hand landmarks 

Finger positions are analyzed

Predefined rules map gestures to actions

Commands are executed using system libraries



⚠️ Requirements


Webcam (mandatory)

Good lighting for accurate detection

Windows OS (for full functionality like brightness & volume control)

Ensure good lighting

Keep hand within camera frame

📈 Future Improvements


🤖 Add ML-based gesture recognition

🖱️ Virtual mouse control

🎮 Gesture gaming

🌐 IoT / Smart home integration

🖥️ GUI interface


📚 Learning Outcomes


Computer Vision basics

Hand tracking using MediaPipe

Real-time system design

Debugging and optimization



🙌 Acknowledgements


MediaPipe by Google

OpenCV community

Python open-source libraries



👨‍💻 Author


Anubhaw Anand Singh

🎓 B.Tech Aerospace Engineering

📘 Registration Number: 25BAS10088



📜 License

This project is open-source and free to use.



🎯 Final Note

This project shows how simple computer vision + logic can create powerful real-world applications 🚀
