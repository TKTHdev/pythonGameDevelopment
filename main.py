from detect import detect
from game import Game
from game2 import Game2
import pyxel


gamemode=detect()
#gamemode=1

if gamemode==1:
    a=Game()



elif gamemode==2:
    a=Game2()



