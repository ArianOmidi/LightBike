from pygame import image

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
TRAILRED = (191, 19, 19)
TRAILBLUE = (117, 164, 255)

BACKGROUND = (10, 10, 10)
GRIDCOLOR = (0, 25, 0)

GRIDLINES = 10

PLAYERLIVES = 3
SPEEDBOOSTFACTOR = 2.0
POWERUPTIME = 5

# --- IMAGES --- #

ONE = image.load("../resources/1.png")
TWO = image.load("../resources/2.png")
THREE = image.load("../resources/3.png")
EXPLOSION = image.load("../resources/explosion.png")

IMAGES = [ONE, TWO, THREE]
for img in IMAGES:
    img.set_colorkey(BLACK)

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

# --- GETTERS --- #

def getTrailColor(color):
    if (color == "RED"):
        return TRAILRED

def getImages(color):
    if (color == "RED"):
        return ["../resources/RedCarU.png", "../resources/RedCarR.png", "../resources/RedCarD.png", "../resources/RedCarL.png"]