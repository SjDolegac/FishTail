import pygame as pg
import random as rd
vec = pg.math.Vector2

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (139, 0, 139)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)

# game options / settings
TITLE = ""
WDTH = 960  # 30 x 32
HGHT = 960  # 30 x 32
FPS = 60
TILESZ = 32
GRDWDTH = WDTH / TILESZ
GRDHGHT = HGHT / TILESZ
BGCOLOR = LIGHTGREY
WALL_IMG = 'Red_Brick.png'

# player settings
PLYR_ACC = 7.25
PLYR_FRCTN = -0.02
#PLYR_SPD = 100
PLYR_ROT_SPD = 250
PLYR_HIT_RECT = pg.Rect(0, 0, 42, 42)
PLYR_IMG = 'Car_Orange.png'
PLYRSZ = 48
BARREL_OFFSET = vec(30, 10)

# gun settings
BULLET_IMG = 'Bullet.png'
BULLET_SPD = 1000
BULLET_LFTIME = 1000
BULLET_RATE = 150
BULLET_HIT_RECT = (0, 0, 2, 2)
KICKBACK = 10 # 200
GUN_SPREAD = 5

# mob settings
MOB_IMG = 'Enemy_Red.png'
MOB_SPD = 700
MOB_FRCTN = -1.00
MOB_HIT_RECT = pg.Rect(0, 0, 42, 42)
