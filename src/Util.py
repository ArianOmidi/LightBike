from pygame import image

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED = (232, 12, 12)
YELLOW = (255, 247, 0)
TRAILRED = (191, 19, 19)
INVISIBLEREDTRAIL = (100, 19, 19)
BOOSTREDTRAIL = (237, 60, 47)
TRAILBLUE =  (117, 164, 255)

BACKGROUND = (10, 10, 10)
GRIDCOLOR = (0, 25, 0)
BORDERCOLOR = (0, 60, 0)

trailSize = 3
playerWidth = 11
BORDERWIDTH = 6
GRIDLINES = 10
# Boost trail divider
divider = 3


PLAYERLIVES = 3
SPEEDBOOSTFACTOR = 3
POWERUPTIME = 4
FPS = 60

# --- IMAGES --- #

ONE = image.load("../resources/1.png")
TWO = image.load("../resources/2.png")
THREE = image.load("../resources/3.png")
EXPLOSION = image.load("../resources/explosion.png")

BIKES = [   [image.load("../resources/RedCarU.png"), image.load("../resources/RedCarR.png"), image.load("../resources/RedCarD.png"), image.load("../resources/RedCarL.png")],
            [image.load("../resources/BlueCarU.png"), image.load("../resources/BlueCarR.png"), image.load("../resources/BlueCarD.png"), image.load("../resources/BlueCarL.png")],
            [image.load("../resources/YellowCarU.png"), image.load("../resources/YellowCarR.png"), image.load("../resources/YellowCarD.png"), image.load("../resources/YellowCarL.png")] ,
            [image.load("../resources/GreenCarU.png"), image.load("../resources/GreenCarR.png"), image.load("../resources/GreenCarD.png"), image.load("../resources/GreenCarL.png")]
         ]

IMAGES = [ONE, TWO, THREE]

for img in IMAGES:
    img.set_colorkey(BLACK)

for color in BIKES:
    for bike in color:
        bike.set_colorkey(WHITE)

# --- FUNCTIONS --- #

def sign(x):
    if (x == 0):
        return 0
    elif (x < 0):
        return -1
    else:
        return 1

def hasValue(x):
    if (x == 0):
        return 0
    else:
        return 1

def ceil(x):
    tmp = int(x)

    if (x == tmp):
        return x
    return tmp + 1

# --- GETTERS --- #

def getTrailColor(color, powerup):
    if (color == "RED"):
        if (powerup == True):
            return RED
        else:
            return RED
    if (color == "YELLOW"):
        return YELLOW

def getPowerup(color):
    if (color == "RED"):
        return "BOOST"

def getImages(color):
    if (color == "RED"):
        return BIKES[0]
    if (color == "BLUE"):
        return BIKES[1]
    if (color == "YELLOW"):
        return BIKES[2]

def isTrue(bool):
    if bool:
        return 1
    else:
        return 0

def getUnitVector(vector):
    return (sign(vector[0]), sign(vector[1]))


