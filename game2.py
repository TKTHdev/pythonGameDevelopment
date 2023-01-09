import random

import cvzone
import pyxel
import cv2
import numpy as np
import math
from cvzone.HandTrackingModule import HandDetector


class incomingObject:
    def __init__(self):
        self.x=200
        self.y=100
        self.ID=random.randrange(0,8)

        if self.ID<=3:
            self.isGarbage=False
        else:
            self.isGarbage=True


    def move(self,Game2):
        self.x-=Game2.difficulty




incomingObjects=[incomingObject()]



class Game2:
    def __init__(self):

        #camera setup
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 720)
        self.cap.set(4, 720)

        self.detector = HandDetector(detectionCon=0.8, maxHands=1)



        #check if your finger is up!!
        self.up=True
        self.difficulty=1

        self.score=0
        self.life=5
        pyxel.init(200, 200, title="Dynamic Action2", fps=15)
        pyxel.run(self.update,self.draw)




    def update(self):

            #define hand
            success, img = self.cap.read()
            hands = self.detector.findHands(img, draw=False)


            #what will be executed when your hand is detected
            if hands:

                lmList = hands[0]["lmList"]
                x, y, w, h = hands[0]['bbox']
                x1 = lmList[5][0]
                y1 = lmList[5][1]

                x2 = lmList[17][0]
                y2 = lmList[17][1]


                hand = hands[0]
                fingers = self.detector.fingersUp(hand)

                X1 = lmList[8][0]
                X2 = lmList[0][0]

                Y1 = lmList[8][1]
                Y2 = lmList[0][1]

                if Y1 > Y2:
                    self.up=False

                else:
                    self.up=True


                for item in incomingObjects:
                    if self.up and item.x>=90 and item.x<=120:
                        if not item.isGarbage:
                            self.score+=10
                        else:
                            self.life-=1

                if self.life==0:
                    pyxel.quit()

                print(self.up)


            cv2.imshow("Image", img)
            cv2.waitKey(1)


    def update_player(self):
        pass

    def draw(self):
        pass

