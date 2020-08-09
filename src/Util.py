from PIL import Image
from pygame import Surface
from pygame import image


# --- CLASSES --- #

class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """

    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """

        # Load the sprite sheet.
        self.sprite_sheet = image.load(file_name)

        x = Image.open(file_name)
        x.convert("RGB")
        self.color = x.getpixel((0,0))

    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

        # Create a new blank image
        image = Surface([width, height]).convert()

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Assuming black works as the transparent color
        image.set_colorkey(self.color)

        # Return the image
        return image

# --- CONSTANTS -- #

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (232, 12, 12)
YELLOW = (255, 247, 0)
GREEN = (0, 255, 0)
TRAILRED = (191, 19, 19)
INVISIBLEREDTRAIL = (100, 19, 19)
BOOSTREDTRAIL = (237, 60, 47)
TRAILBLUE =  (117, 164, 255)

BACKGROUND =  (10, 10, 10)
GRIDCOLOR = (0, 25, 0)
BORDERCOLOR = (0, 50, 0)

trailSize = 3
playerWidth = 11
PLAYERWIDTH = 11
BORDERWIDTH = 5
GRIDLINES = 10
# Boost trail divider
divider = 3


PLAYERLIVES = 3
SPEEDBOOSTFACTOR = 3
POWERUPTIME = 4
JUMPTIME = 0.5
FPS = 60

# --- IMAGES --- #

ONE = image.load("../resources/1.png")
TWO = image.load("../resources/2.png")
THREE = image.load("../resources/3.png")
EXPLOSION = image.load("../resources/explosion.png")

BIKES_SHEET = SpriteSheet("../resources/bikes_sprite_sheet.png")
POWERUP_BIKES_SHEET = SpriteSheet("../resources/bikes_sprite_sheet_powerup.png")

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
    elif (color == "YELLOW"):
        return YELLOW
    elif (color == "BLUE"):
        return TRAILBLUE
    elif (color == "GREEN"):
        return GREEN

def getPowerup(color):
    if (color == "RED"):
        return "BOOST"

def getBike(dir, color):
    if (color == "RED"):
        if dir[0] > 0:
            return BIKES_SHEET.get_image(0, 13 * PLAYERWIDTH, 2 * PLAYERWIDTH, PLAYERWIDTH)
        elif dir[0] < 0:
            return BIKES_SHEET.get_image(0, 12 * PLAYERWIDTH, 2 * PLAYERWIDTH, PLAYERWIDTH)
        else:
            if dir[1] > 0:
                return BIKES_SHEET.get_image(0, 4 * PLAYERWIDTH, PLAYERWIDTH, 2 * PLAYERWIDTH)
            else:
                return BIKES_SHEET.get_image(PLAYERWIDTH, 4 * PLAYERWIDTH, PLAYERWIDTH, 2 * PLAYERWIDTH)
    elif (color == "BLUE"):
        if dir[0] > 0:
            return BIKES_SHEET.get_image(0, 9 * PLAYERWIDTH, 2 * PLAYERWIDTH, PLAYERWIDTH)
        elif dir[0] < 0:
            return BIKES_SHEET.get_image(0, 8 * PLAYERWIDTH, 2 * PLAYERWIDTH, PLAYERWIDTH)
        else:
            if dir[1] > 0:
                return BIKES_SHEET.get_image(0, 0, PLAYERWIDTH, 2 * PLAYERWIDTH)
            else:
                return BIKES_SHEET.get_image(PLAYERWIDTH, 0, PLAYERWIDTH, 2 * PLAYERWIDTH)
    elif (color == "YELLOW"):
        if dir[0] > 0:
            return BIKES_SHEET.get_image(0, 15 * PLAYERWIDTH, 2 * PLAYERWIDTH, PLAYERWIDTH)
        elif dir[0] < 0:
            return BIKES_SHEET.get_image(0, 14 * PLAYERWIDTH, 2 * PLAYERWIDTH, PLAYERWIDTH)
        else:
            if dir[1] > 0:
                return BIKES_SHEET.get_image(0, 6 * PLAYERWIDTH, PLAYERWIDTH, 2 * PLAYERWIDTH)
            else:
                return BIKES_SHEET.get_image(PLAYERWIDTH, 6 * PLAYERWIDTH, PLAYERWIDTH, 2 * PLAYERWIDTH)
    elif (color == "GREEN"):
        if dir[0] > 0:
            return BIKES_SHEET.get_image(0, 11 * PLAYERWIDTH, 2 * PLAYERWIDTH, PLAYERWIDTH)
        elif dir[0] < 0:
            return BIKES_SHEET.get_image(0, 10 * PLAYERWIDTH, 2 * PLAYERWIDTH, PLAYERWIDTH)
        else:
            if dir[1] > 0:
                return BIKES_SHEET.get_image(0, 2 * PLAYERWIDTH, PLAYERWIDTH, 2 * PLAYERWIDTH)
            else:
                return BIKES_SHEET.get_image(PLAYERWIDTH, 2 * PLAYERWIDTH, PLAYERWIDTH, 2 * PLAYERWIDTH)
    else:
        return getPowerupBike(dir, color)

def getPowerupBike(dir, color):
    if (color == "POWERUP_RED"):
        if dir[0] > 0:
            return POWERUP_BIKES_SHEET.get_image(0, 13 * PLAYERWIDTH, 2 * PLAYERWIDTH, PLAYERWIDTH)
        elif dir[0] < 0:
            return POWERUP_BIKES_SHEET.get_image(0, 12 * PLAYERWIDTH, 2 * PLAYERWIDTH, PLAYERWIDTH)
        else:
            if dir[1] > 0:
                return POWERUP_BIKES_SHEET.get_image(0, 4 * PLAYERWIDTH, PLAYERWIDTH, 2 * PLAYERWIDTH)
            else:
                return POWERUP_BIKES_SHEET.get_image(PLAYERWIDTH, 4 * PLAYERWIDTH, PLAYERWIDTH, 2 * PLAYERWIDTH)
    elif (color == "POWERUP_BLUE"):
        if dir[0] > 0:
            return POWERUP_BIKES_SHEET.get_image(0, 9 * PLAYERWIDTH, 2 * PLAYERWIDTH, PLAYERWIDTH)
        elif dir[0] < 0:
            return POWERUP_BIKES_SHEET.get_image(0, 8 * PLAYERWIDTH, 2 * PLAYERWIDTH, PLAYERWIDTH)
        else:
            if dir[1] > 0:
                return POWERUP_BIKES_SHEET.get_image(0, 0, PLAYERWIDTH, 2 * PLAYERWIDTH)
            else:
                return POWERUP_BIKES_SHEET.get_image(PLAYERWIDTH, 0, PLAYERWIDTH, 2 * PLAYERWIDTH)
    elif (color == "POWERUP_YELLOW"):
        if dir[0] > 0:
            return POWERUP_BIKES_SHEET.get_image(0, 15 * PLAYERWIDTH, 2 * PLAYERWIDTH, PLAYERWIDTH)
        elif dir[0] < 0:
            return POWERUP_BIKES_SHEET.get_image(0, 14 * PLAYERWIDTH, 2 * PLAYERWIDTH, PLAYERWIDTH)
        else:
            if dir[1] > 0:
                return POWERUP_BIKES_SHEET.get_image(0, 6 * PLAYERWIDTH, PLAYERWIDTH, 2 * PLAYERWIDTH)
            else:
                return POWERUP_BIKES_SHEET.get_image(PLAYERWIDTH, 6 * PLAYERWIDTH, PLAYERWIDTH, 2 * PLAYERWIDTH)
    elif (color == "POWERUP_GREEN"):
        if dir[0] > 0:
            return POWERUP_BIKES_SHEET.get_image(0, 11 * PLAYERWIDTH, 2 * PLAYERWIDTH, PLAYERWIDTH)
        elif dir[0] < 0:
            return POWERUP_BIKES_SHEET.get_image(0, 10 * PLAYERWIDTH, 2 * PLAYERWIDTH, PLAYERWIDTH)
        else:
            if dir[1] > 0:
                return POWERUP_BIKES_SHEET.get_image(0, 2 * PLAYERWIDTH, PLAYERWIDTH, 2 * PLAYERWIDTH)
            else:
                return POWERUP_BIKES_SHEET.get_image(PLAYERWIDTH, 2 * PLAYERWIDTH, PLAYERWIDTH, 2 * PLAYERWIDTH)

def isTrue(bool):
    if bool:
        return 1
    else:
        return 0

def getUnitVector(vector):
    return (sign(vector[0]), sign(vector[1]))




