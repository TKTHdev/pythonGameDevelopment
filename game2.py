import random
import pyttsx3
import cvzone
import pyxel
import cv2
import numpy as np
import math
from cvzone.HandTrackingModule import HandDetector
from playsound import playsound


difficulty=5


class incomingObject:
    def __init__(self):
        self.x=200
        self.y=45
        self.ID=random.randrange(0,8)

        self.caught=False



        if self.ID<=3:
            self.isGarbage=False
            self.startX=32
        else:
            self.isGarbage=True
            self.startX=48

        self.clear=False
        self.difficulty=5


    def move(self):
        self.x-=difficulty

    def get(self):
        self.x-=10
        self.y-=10


objectXList=[64,80,96,112,64,80,96,112]

incomingObjects=[incomingObject()]



class Game2:
    def __init__(self):

        #camera setup
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 720)
        self.cap.set(4, 720)

        self.detector = HandDetector(detectionCon=0.8, maxHands=1)

        self.engine=pyttsx3.init()

        #check if your finger is up!!
        self.up=True

        self.difficulty=5

        self.score=0
        self.life=5

        self.count=0



        pyxel.init(200, 200, title="Dynamic Action2", fps=15)
        pyxel.load("assets/art2.pyxres")
        pyxel.run(self.update,self.draw)




    def update(self):
            global difficulty

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

                if not item.caught:
                    item.move()
                else:
                    item.get()

                if self.up and item.x >= 88 and item.x <= 102 and not item.clear:
                    if not item.isGarbage:
                        self.score += 10
                        if self.score%50==0:
                            difficulty+=1
                        item.clear = True
                        item.caught=True
                    else:
                        item.clear = True
                        item.caught=True

            self.count+=pyxel.rndi(1,11)



            if self.count%10==0:
                hello=incomingObject()
                incomingObjects.append(hello)

            cv2.imshow("Image", img)
            cv2.waitKey(1)

    def draw(self):
        pyxel.cls(3)


        pyxel.circ(100,50,10,7)
        pyxel.circ(100,50,8,6)
        pyxel.circ(100,50,6,5)

        if self.up:
            pyxel.blt(80,20,0,21,91,6,7,7)
        else:
            pyxel.blt(97,47,0,21,91,6,7,7)


        for obj in incomingObjects:
                pyxel.blt(obj.x,obj.y,0,obj.startX,objectXList[obj.ID],16,16,11)

        pyxel.text(0,30,"LIFE",0)
        pyxel.text(40,30,f"{str(self.life)}",0)

        pyxel.text(0,50,"SCORE",0)
        pyxel.text(40,50,f"{str(self.score)}",0)

