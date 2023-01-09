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
        self.y=45
        self.ID=random.randrange(0,8)



        if self.ID<=3:
            self.isGarbage=False
            self.startX=32
        else:
            self.isGarbage=True
            self.startX=48

        self.clear=False


    def move(self):
        self.x-=5


objectXList=[64,80,96,112,64,80,96,112]

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


        self.score=0
        self.life=5

        self.count=0



        pyxel.init(200, 200, title="Dynamic Action2", fps=15)
        pyxel.load("assets/art2.pyxres")
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




                if self.life==0:
                    pyxel.quit()

                print(self.up)

            for item in incomingObjects:

                item.move()

                if self.up and item.x >= 90 and item.x <= 120 and not item.clear:
                    if not item.isGarbage:
                        self.score += 10
                        item.clear = True
                    else:
                        self.life -= 1
                        item.clear = True

            self.count+=pyxel.rndi(1,11)



            if self.count%10==0:
                hello=incomingObject()
                incomingObjects.append(hello)

            cv2.imshow("Image", img)
            cv2.waitKey(1)


    def update_player(self):
        pass


    def draw(self):
        pyxel.cls(3)

        pyxel.circ(100,50,10,7)
        pyxel.circ(100,50,8,6)
        pyxel.circ(100,50,6,5)


        for obj in incomingObjects:
            if not obj.clear:
                pyxel.blt(obj.x,obj.y,0,obj.startX,objectXList[obj.ID],16,16,11)

