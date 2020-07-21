BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
TRAILRED = (191, 19, 19)

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

def getImages(color):
    if (color == RED):
        return ["../resources/RedCarU.png", "../resources/RedCarR.png", "../resources/RedCarD.png", "../resources/RedCarL.png"]