import cv2 as cv
import mediapipe as mp
from enum import Enum
import numpy as np
import pyautogui 
import threading

class Indecies(Enum):
    WRIST = 0
    THUMB_CNC = 1
    THUMB_MCP = 2
    THUMB_IP = 3
    THUMB_TIP = 4
    INDEX_MCP = 5
    INDEX_PIP = 6
    INDEX_DIP = 7
    INDEX_TIP = 8
    MIDDLE_MCP = 9
    MIDDLE_PIP = 10
    MIDDLE_DIP = 11
    MIDDLE_TIP = 12
    RING_MCP = 13
    RING_PIP = 14
    RING_DIP = 15
    RING_TIP = 16
    PINKY_MCP = 17
    PINKY_PIP = 18
    PINKY_DIP = 19
    PINKY_TIP = 20

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands = 1)

xResolution = pyautogui.size()[0]
yResolution = pyautogui.size()[1]

detectionRadius = 50

mouseX = 100
mouseY = 100

middleX = 0
middleY = 0

ringX = 0
ringY = 0

thumbX = 0
thumbY = 0

pinkymcp = 0
indexmcp = 0

pyautogui.FAILSAFE = False

def moveMouse():
    middleClickDist = np.sqrt(np.power(thumbX - middleX, 2) + np.power(thumbY - middleY, 2))
    ringClickDist = np.sqrt(np.power(thumbX - ringX, 2) + np.power(thumbY - ringY, 2))

    detectionRadius = 50 * (np.abs(indexmcp - pinkymcp) * 10)

    print(detectionRadius)

    if middleClickDist < detectionRadius:
        print("Click")
        pyautogui.click()


    if ringClickDist < detectionRadius:
        print("Click")
        pyautogui.click(button="right")

    pyautogui.moveTo(mouseX, mouseY)

def processFrame():
    success, frame = video.read()
    frame = cv.flip(frame, 1)

    frame.flags.writeable = False

    RGBframe = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    
    results = hands.process(RGBframe)

    global mouseX, mouseY, middleX, middleY, thumbX, thumbY, ringX, ringY, pinkymcp, indexmcp

    if results.multi_hand_landmarks:
        for handLandmarks in results.multi_hand_landmarks:
            for id, lm in enumerate(handLandmarks.landmark):
                if id == Indecies.INDEX_TIP.value: 
                    mouseX = lm.x * xResolution
                    mouseY = lm.y * yResolution
                elif id == Indecies.MIDDLE_TIP.value:
                    middleX = lm.x * xResolution
                    middleY = lm.y * yResolution
                elif id == Indecies.THUMB_TIP.value:
                    thumbX = lm.x * xResolution
                    thumbY = lm.y * yResolution
                elif id == Indecies.RING_TIP.value:
                    ringX = lm.x * xResolution
                    ringY = lm.y * yResolution
                elif id == Indecies.PINKY_MCP.value:
                    pinkymcp = lm.x
                elif id == Indecies.INDEX_MCP.value:
                    indexmcp = lm.x

video = cv.VideoCapture(0)

if __name__ == "__main__":
    while True:
        frameProcess = threading.Thread(target = processFrame)
        mouseProcess = threading.Thread(target = moveMouse)
    
        frameProcess.start()
        mouseProcess.start()
    
        frameProcess.join()
        mouseProcess.join()
