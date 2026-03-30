import cv2
import mediapipe as mp
import numpy as np
import time
import pyautogui
import screen_brightness_control as sbc

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#  AUDIO SETUP 
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None
)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volMin, volMax = volume.GetVolumeRange()[:2]

#  MEDIAPIPE 
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

#  CAMERA 
cap = cv2.VideoCapture(0)

# VARIABLES 
pTime = 0
last_brightness_time = 0

gesture_buffer = []
buffer_size = 5
prev_gesture = None
gesture_text = ""

# FUNCTIONS 
def fingers_up(lmList):
    fingers = []

    # Thumb
    if lmList[4][1] > lmList[3][1]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    tips = [8, 12, 16, 20]
    for tip in tips:
        if lmList[tip][2] < lmList[tip - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers


def get_gesture(fingers):
    if fingers == [0,0,0,0,0]:
        return "FIST"
    elif fingers == [1,1,1,1,1]:
        return "OPEN"
    elif fingers == [0,1,0,0,0]:
        return "NEXT"
    elif fingers == [1,0,0,0,0]:
        return "PREV"
    else:
        return "NONE"


# LOOP 
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    lmList = []

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    if len(lmList) != 0:

        fingers = fingers_up(lmList)

        #  VOLUME CONTROL 
        x1, y1 = lmList[4][1], lmList[4][2]   # Thumb
        x2, y2 = lmList[8][1], lmList[8][2]   # Index

        length = np.hypot(x2 - x1, y2 - y1)
        vol = np.interp(length, [30, 200], [volMin, volMax])
        volBar = np.interp(length, [30, 200], [400, 150])
        volPer = np.interp(length, [30, 200], [0, 100])

        volume.SetMasterVolumeLevel(vol, None)

        cv2.rectangle(img, (50,150), (85,400), (0,255,0), 3)
        cv2.rectangle(img, (50,int(volBar)), (85,400), (0,255,0), cv2.FILLED)
        cv2.putText(img, "VOLUME", (40,140),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        cv2.putText(img, f'{int(volPer)}%', (40,450),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 3)

        #  BRIGHTNESS CONTROL 
        x3, y3 = lmList[12][1], lmList[12][2]  # Middle finger

        length_b = np.hypot(x3 - x1, y3 - y1)
        brightness = np.interp(length_b, [30, 200], [0, 100])
        bar = np.interp(length_b, [30,200], [400,150])

        if time.time() - last_brightness_time > 0.3:
            sbc.set_brightness(int(brightness))
            last_brightness_time = time.time()

        cv2.rectangle(img, (150,150), (185,400), (255,0,0), 3)
        cv2.rectangle(img, (150,int(bar)), (185,400), (255,0,0), cv2.FILLED)
        cv2.putText(img, "BRIGHTNESS", (130,140),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)
        cv2.putText(img, f'{int(brightness)}%', (130,450),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 3)

        #  GESTURE DETECTION
        current_gesture = get_gesture(fingers)

        gesture_buffer.append(current_gesture)
        if len(gesture_buffer) > buffer_size:
            gesture_buffer.pop(0)

        if gesture_buffer.count(current_gesture) == buffer_size:

            if current_gesture != prev_gesture:

                if current_gesture == "FIST":
                    pyautogui.press("volumemute")
                    pyautogui.press("playpause")
                    gesture_text = "MUTE / PAUSE"

                elif current_gesture == "OPEN":
                    pyautogui.press("playpause")
                    gesture_text = "PLAY"

                elif current_gesture == "NEXT":
                    pyautogui.press("nexttrack")
                    gesture_text = "NEXT TRACK"

                elif current_gesture == "PREV":
                    pyautogui.press("prevtrack")
                    gesture_text = "PREVIOUS TRACK"

                prev_gesture = current_gesture

    #  UI DISPLAY 
    cv2.rectangle(img, (350, 20), (640, 100), (0, 0, 0), -1)

    cv2.putText(img, f'Gesture: {gesture_text}', (360, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,255), 2)

    #  FPS 
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (500,450),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,255), 2)

    cv2.imshow("AI Gesture Control System", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()