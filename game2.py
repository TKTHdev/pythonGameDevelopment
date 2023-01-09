import random

import cvzone
import pyxel
import cv2
import numpy as np
import math
from cvzone.HandTrackingModule import HandDetector





class Game2:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 720)
        self.cap.set(4, 720)

        self.detector = HandDetector(detectionCon=0.8, maxHands=1)

        self.disT = [300, 245, 200170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
        self.cmDisT = [20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 75, 80, 85, 90, 95, 100]

        pyxel.init(200, 200, title="Dynamic Action2", fps=15)
        self.coff = np.polyfit(self.disT, self.cmDisT, 2)
        pyxel.run(self.update,self.draw)


        self.up=True



    def update(self):
        success, img = self.cap.read()
        hands = self.detector.findHands(img, draw=False)

        if hands:
            success, img = self.cap.read()
            hands = self.detector.findHands(img, draw=False)

            if hands:
                lmList = hands[0]["lmList"]
                x, y, w, h = hands[0]['bbox']
                x1 = lmList[5][0]
                y1 = lmList[5][1]

                x2 = lmList[17][0]
                y2 = lmList[17][1]

                self.distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
                A, B, C = self.coff
                centimeterD = A * self.distance + B * self.distance + C

                hand = hands[0]
                fingers = self.detector.fingersUp(hand)

                X1 = lmList[8][0]
                X2 = lmList[0][0]

                Y1 = lmList[8][1]
                Y2 = lmList[0][1]

                if Y1 > Y2:
                    self.up=True
                else:
                    self.up=False

                cvzone.putTextRect(img, f'{int(centimeterD)}cm //// ', (x, y))

            cv2.imshow("Image", img)
            cv2.waitKey(1)


    def update_player(self):
        pass

    def draw(self):
        pass

