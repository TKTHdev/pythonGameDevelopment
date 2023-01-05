import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import math
import numpy
import cvzone
import time
import datetime

def detect():
    cap=cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)

    detector=HandDetector(detectionCon=0.8,maxHands=2)

    disT=[300,245,200170,145,130,112,103,93,87,80,75,70,67,62,59,57]
    cmDisT=[20,25,30,35,40,45,50,55,60,70,75,80,85,90,95,100]

    coff=np.polyfit(disT,cmDisT,2)

    upperRight = "upperRight"
    upperLeft = "upperLeft"
    bottomRight = "bottomRight"
    bottomLeft = "bottomLeft"

    uR=False
    uL=False
    bR=False
    bL=False
    started=False

    while True:
        success,img=cap.read()
        hands=detector.findHands(img,draw=False)





        if hands:
            lmList=hands[0]["lmList"]
            x,y,w,h=hands[0]['bbox']
            x1=lmList[5][0]
            y1=lmList[5][1]

            x2=lmList[17][0]
            y2=lmList[17][1]
            print(x1,y1)

            if (100<x1<200 and 100<y1<200):
                #upperLeft="OK!"
                uL=True

            if (1050<x1<1250 and 100<y1<200):
                #upperRight="OK!"
                uR=True

            if (1050<x1<1250 and 600<y1<700):
                #bottomRight="OK!"
                bR=True

            if (100<x1<200 and 600<y1<700):
                #bottomLeft="OK!"
                bL=True

            distance=int(math.sqrt((y2-y1)**2+(x2-x1)**2))
            A,B,C=coff
            centimeterD=A*distance+B*distance+C

            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),3)
            cvzone.putTextRect(img,f'{int(centimeterD) }cm  (70cm is ok)',(x,y))
        if not uL:
            cvzone.putTextRect(img, upperLeft, (100, 100))

        if not uR:
            cvzone.putTextRect(img, upperRight, (100, 200))

        if not bL:
            cvzone.putTextRect(img, bottomLeft, (100, 300))

        if not bR:
            cvzone.putTextRect(img, bottomRight, (100, 400))

        if not started and uL and uR and bL and bR:
            return True
            break;



        cv2.imshow("Image",img)
        cv2.waitKey(1)
