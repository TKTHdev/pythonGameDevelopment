import random

import cvzone
import pyxel
import cv2
import numpy as np
import math
from cvzone.HandTrackingModule import HandDetector

class CheckBall:
    def __init__(self,y):
        self.x=30
        self.y=y
        self.clear=False;


checkballs=[CheckBall(5),CheckBall(195)]



class incomingItem:
    def __init__(self,y,angular):
        self.x=200
        self.y=y
        self.angular=angular
        self.vx=pyxel.cos(angular)
        self.vy=pyxel.sin(angular)
        self.incomingSpeed=4
        self.houkou=200

    def move(self):
        self.x-=self.vx * self.incomingSpeed
        self.y-=self.vy * self.incomingSpeed

        if self.y>200 or self.y<0:
            self.vy*=-1

    def catched(self):
        self.x=200
        self.y=random.randrange(20,180)
        self.angular=random.randrange(15,75)
        self.vx=pyxel.cos(self.angular)
        self.vy=pyxel.sin(self.angular)




firsty=random.randrange(20,180)
firstAngular=random.randrange(30,75)

incomingItems=[incomingItem(firsty,firstAngular)]




class Game:
    def __init__(self):

        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 720)
        self.cap.set(4, 720)

        self.detector=HandDetector(detectionCon=0.8,maxHands=1)

        self.disT=[300,245,200170,145,130,112,103,93,87,80,75,70,67,62,59,57]
        self.cmDisT=[20,25,30,35,40,45,50,55,60,70,75,80,85,90,95,100]
        pyxel.init(200,200,title="Dynamic Action2",fps=15)

        self.y=100
        self.is_alive=True
        self.started=False


        self.point=0


        

        self.coff=np.polyfit(self.disT,self.cmDisT,2)

        pyxel.run(self.update,self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.update_player()

        for ball in checkballs:
            if self.y>=ball.y-5 and self.y<=ball.y+5:
                ball.clear=True

        if checkballs[0].clear and checkballs[1].clear:

            for incomingBall in incomingItems:
                incomingBall.move()

                if incomingBall.x<0:
                    incomingBall.x=200

                if self.y+7>=incomingBall.y and  self.y-7<=incomingBall.y and 37>=incomingBall.x and 23<=incomingBall.x:
                    incomingBall.catched()
                    self.point+=1

                    if self.point%3==0:
                        ball=incomingItem(random.randrange(20,180),random.randrange(15,75))
                        incomingItems.append(ball)






    def update_player(self):

        success,img=self.cap.read()
        hands=self.detector.findHands(img,draw=False)









        if hands:
            lmList=hands[0]["lmList"]
            x,y,w,h=hands[0]['bbox']
            x1=lmList[5][0]
            y1=lmList[5][1]

            x2=lmList[17][0]
            y2=lmList[17][1]

            self.distance=int(math.sqrt((y2-y1)**2+(x2-x1)**2))
            A,B,C=self.coff
            centimeterD=A*self.distance+B*self.distance+C
            cvzone.putTextRect(img,f'{int(centimeterD) }cm  (70cm is ok)',(x,y))
            self.y=100+5*(66-centimeterD)
        cv2.imshow("Image",img)
        cv2.waitKey(1)


    def draw(self):
        pyxel.cls(7)

        pyxel.text(0,10,"points:",5)
        pyxel.text(40,10,str(self.point),5)

        for ball in checkballs:
            if not ball.clear:
                pyxel.circ(20,ball.y,10,6)

        for incoming in incomingItems:
            pyxel.circ(incoming.x,incoming.y,10,6)

        #pyxel.rect(10,self.y-20,10,40,8)
        pyxel.circ(30,self.y,15,3)

