import random

import cvzone
import pyxel
import cv2
import numpy as np
import math
from cvzone.HandTrackingModule import HandDetector

iti=0

class CheckBall:
    def __init__(self, y):
        self.x = 30
        self.y = y
        self.clear = False;


checkballs = [CheckBall(5), CheckBall(185)]


class incomingItem:
    def __init__(self, y, angular):
        self.x = 200
        self.y = y
        self.angular = angular
        self.vx = pyxel.cos(angular)
        self.vy = pyxel.sin(angular)
        self.incomingSpeed = 4
        self.houkou = 200

    def move(self):
        self.x -= self.vx * self.incomingSpeed
        self.y -= self.vy * self.incomingSpeed

        if self.y > 200 or self.y < 0:
            self.vy *= -1

    def catched(self):
        self.x = 200
        self.y = random.randrange(20, 180)
        self.angular = random.randrange(15, 55)
        self.vx = pyxel.cos(self.angular)
        self.vy = pyxel.sin(self.angular)




firsty = random.randrange(20, 180)
firstAngular = random.randrange(30, 55)

incomingItems = [incomingItem(firsty, firstAngular)]

class helpItem:
    def __init__(self, y, angular):
        self.x = 200
        self.y = y
        self.angular = angular
        self.vx = pyxel.cos(angular)
        self.vy = pyxel.sin(angular)
        self.incomingSpeed = 4
        self.houkou = 200

    def move(self):
        self.x -= self.vx * self.incomingSpeed
        self.y -= self.vy * self.incomingSpeed

        if self.y > 200 or self.y < 0:
            self.vy *= -1



helpItems=[]

class Game:
    def __init__(self):


        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 720)
        self.cap.set(4, 720)

        self.detector = HandDetector(detectionCon=0.8, maxHands=1)

        self.disT = [300, 245, 200170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
        self.cmDisT = [20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 75, 80, 85, 90, 95, 100]
        pyxel.init(200, 200, title="Dynamic Action2", fps=15)
        pyxel.load("assets/art2.pyxres")
        self.x=30

        self.y = 100
        self.is_alive = True
        self.started = False

        self.point = 0
        self.score=5

        self.hit = False
        self.moveCount = 0

        self.backcol=1

        self.cl1=pyxel.rndi(3,11)
        self.cl2=pyxel.rndi(3,11)

        self.coff = np.polyfit(self.disT, self.cmDisT, 2)
        pyxel.playm(1,loop=True)
        pyxel.run(self.update, self.draw)





    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.update_player()

        for ball in checkballs:
            if self.y >= ball.y - 5 and self.y <= ball.y + 5:
                ball.clear = True

        if checkballs[0].clear and checkballs[1].clear:

            for incomingBall in incomingItems:
                incomingBall.move()

                if incomingBall.x < 0:
                    incomingBall.x = 200
                    self.point+=1
                    if self.point%4*len(incomingItems)==0:
                        ball = incomingItem(random.randrange(20, 180), random.randrange(15, 75))
                        incomingItems.append(ball)

                    luckNum=pyxel.rndi(0,3)
                    if luckNum%3==0:
                        newLuck=helpItem(random.randrange(20, 180), random.randrange(15, 75))
                        helpItems.append(newLuck)

                if self.y +25>= incomingBall.y+7and self.y  <= incomingBall.y+7 and 65 >= incomingBall.x+7 and 30<= incomingBall.x+7:
                    incomingBall.catched()
                    self.cl1=pyxel.rndi(3,11)
                    self.cl2=pyxel.rndi(3,11)
                    self.hit=True
                    self.moveCount=0
                    self.score-=1
                    if self.score==0:
                            pyxel.quit()



        for incomingBall in helpItems:
                incomingBall.move()

                if incomingBall.x < 0:
                    incomingBall.x = 200
                    self.point+=1
                    if self.point%4*len(incomingItems)==0:
                        ball = incomingItem(random.randrange(20, 180), random.randrange(15, 75))
                        incomingItems.append(ball)



                if self.y +25>= incomingBall.y+5and self.y  <= incomingBall.y+5 and 65 >= incomingBall.x+5 and 30<= incomingBall.x+5:
                    self.point+=5
                    incomingBall.x=-10





    def update_player(self):

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


            hand=hands[0]
            fingers=self.detector.fingersUp(hand)

            X1=lmList[8][0]
            X2=lmList[0][0]

            Y1=lmList[8][1]
            Y2=lmList[0][1]

            if Y1>Y2:
                self.y=min(self.y+5,185)
                self.status="DOWN"
                if self.hit:
                    self.moveCount+=1
                    if self.moveCount%10==0:
                        self.moveCount=0
                        self.hit=False

            else:
                self.y=max(self.y-5,0)
                self.status="UP"
                if self.hit:
                    self.moveCount+=1
                    if self.hit%10==0:
                        self.moveCount=0
                        self.hit=False


            cvzone.putTextRect(img, f'{int(centimeterD)}cm //// {self.status}', (x, y))

        cv2.imshow("Image", img)
        cv2.waitKey(1)

    def draw(self):


        global iti

        pyxel.cls(7)

        for i in range(0,200,20):
            for j in range(0,200,20):
                if ((i+j)/20)%2==0:
                    pyxel.blt(i,j,0,0,56,20,20)
                else:
                    pyxel.rect(i,j,20,20,self.cl2)



        for ball in checkballs:
            if not ball.clear:
                pyxel.circ(20, ball.y, 10, 6)
                pyxel.text(0,100,"Eat the food up and down to start the game!!",0)

        for incoming in incomingItems:
            pyxel.blt(incoming.x,incoming.y,0,40,8,15,15,1)

        if self.hit:
            pyxel.blt(self.x,self.y,0,0,0,32,32,0)

        else:
            pyxel.blt(self.x,self.y,0,4,35,25,20,15)

        for helpItem in helpItems:
            pyxel.blt(helpItem.x,helpItem.y,0,43,41,11,11,1)

        pyxel.text(0,10,"SCORE:",0)
        pyxel.text(40,10,str(self.point),0)

        pyxel.text(0,30,"LIFE:",0)
        pyxel.text(40,30,str(self.score),0)