from detect import detect
from game import Game
from game2 import Game2
import pyxel
from playsound import playsound

while True:
    #playsound("assets/annnai.wav")
    gamemode=detect()
    #gamemode=1

    if gamemode==1:
        #playsound("assets/game1.wav")
        a=Game()



    elif gamemode==2:
        #playsound("assets/game2.wav")
        a=Game2()


