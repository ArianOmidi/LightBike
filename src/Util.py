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


""" --- CONSTANTS --- """

# --- COLORS --- #
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = (10, 10, 10)
GRIDCOLOR = (0, 25, 0)
BORDERCOLOR = (0, 50, 0)

# --- TRAIL COLORS --- #
RED = (232, 12, 12)
TRAILRED = (191, 19, 19)
BOOSTREDTRAIL = (237, 60, 47)
YELLOW = (255, 247, 0)
GREEN = (0, 255, 0)
TRAILBLUE =  (117, 164, 255)

# --- DESIGN VARIABLES --- #
BORDER_WIDTH = 5
GRIDLINES = 10

""" --- PLAYER VARIABLES --- """

PLAYER_WIDTH = 11
TRAIL_SIZE = 3
PLAYER_LIVES = 3
VELOCITY = 2

# --- BOOSTER --- #
BOOST_TRAIL_DIVIDER = 3
SPEED_BOOST_FACTOR = 3
BOOSTER_POWERUP_TIME = 3
BOOSTER_POWERUP_NUM = 3

# --- JUMPER --- #
JUMP_TIME = 0.5
JUMPER_POWERUP_TIME = 4
JUMPER_POWERUP_NUM = 3

# --- INVISIBLE --- #
INVISIBLE_POWERUP_TIME = 2.5
INVISIBLE_POWERUP_NUM = 3

# --- BUILDER --- #
BUILDER_POWERUP_TIME = 1.5
WALL_SPEED_FACTOR = 2
BUILDER_POWERUP_NUM = 5

""" --- GAME VARIABLES --- """
FPS = 100
SCREEN_HEIGHT = 750
SCREEN_WIDTH = 1400
BORDER_TOP_OFFSET = 50
PLAYER_ONE_STARTING_POS = (SCREEN_WIDTH * 1 / 10, (SCREEN_HEIGHT + BORDER_TOP_OFFSET - PLAYER_WIDTH) / 5)
PLAYER_TWO_STARTING_POS = (
SCREEN_WIDTH * 9 / 10 - 2 * PLAYER_WIDTH, (SCREEN_HEIGHT + BORDER_TOP_OFFSET - PLAYER_WIDTH) * 4 / 5)

""" --- IMAGES --- """

ONE = image.load("../resources/1.png")
TWO = image.load("../resources/2.png")
THREE = image.load("../resources/3.png")
EXPLOSION = image.load("../resources/explosion.png")

HEART = image.load("../resources/heart.png")
EMPTY_HEART = image.load("../resources/empty_heart.png")

POWERUP_ICON = image.load("../resources/powerup_icon.png")
EMPTY_POWERUP_ICON = image.load("../resources/empty_powerup_icon.png")

PLAYER_ICON_IMAGES = [HEART, EMPTY_HEART]

BIKES_SHEET = SpriteSheet("../resources/bikes_sprite_sheet.png")
POWERUP_BIKES_SHEET = SpriteSheet("../resources/bikes_sprite_sheet_powerup.png")
ICON_BIKES_SHEET = SpriteSheet("../resources/icon_bikes_sprite_sheet.png")

IMAGES = [ONE, TWO, THREE]

for img in IMAGES:
    img.set_colorkey(BLACK)

for img in PLAYER_ICON_IMAGES:
    img.set_colorkey(WHITE)

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


def isTrue(bool):
    if bool:
        return 1
    else:
        return 0

# --- GETTERS --- #

def getTrailColor(color, powerup):
    if (color == "RED"):
        return RED
    elif (color == "YELLOW"):
        return YELLOW
    elif (color == "BLUE"):
        return TRAILBLUE
    elif (color == "GREEN"):
        return GREEN


def getNumOfPowerups(type):
    if (type == "BOOSTER"):
        return BOOSTER_POWERUP_NUM
    elif (type == "BUILDER"):
        return BUILDER_POWERUP_NUM
    elif (type == "INVISIBLE"):
        return INVISIBLE_POWERUP_NUM
    elif (type == "JUMPER"):
        return JUMPER_POWERUP_NUM

def getBike(dir, color):
    if (color == "RED"):
        if dir[0] > 0:
            return BIKES_SHEET.get_image(0, 13 * PLAYER_WIDTH, 2 * PLAYER_WIDTH, PLAYER_WIDTH)
        elif dir[0] < 0:
            return BIKES_SHEET.get_image(0, 12 * PLAYER_WIDTH, 2 * PLAYER_WIDTH, PLAYER_WIDTH)
        else:
            if dir[1] > 0:
                return BIKES_SHEET.get_image(0, 4 * PLAYER_WIDTH, PLAYER_WIDTH, 2 * PLAYER_WIDTH)
            else:
                return BIKES_SHEET.get_image(PLAYER_WIDTH, 4 * PLAYER_WIDTH, PLAYER_WIDTH, 2 * PLAYER_WIDTH)
    elif (color == "BLUE"):
        if dir[0] > 0:
            return BIKES_SHEET.get_image(0, 9 * PLAYER_WIDTH, 2 * PLAYER_WIDTH, PLAYER_WIDTH)
        elif dir[0] < 0:
            return BIKES_SHEET.get_image(0, 8 * PLAYER_WIDTH, 2 * PLAYER_WIDTH, PLAYER_WIDTH)
        else:
            if dir[1] > 0:
                return BIKES_SHEET.get_image(0, 0, PLAYER_WIDTH, 2 * PLAYER_WIDTH)
            else:
                return BIKES_SHEET.get_image(PLAYER_WIDTH, 0, PLAYER_WIDTH, 2 * PLAYER_WIDTH)
    elif (color == "YELLOW"):
        if dir[0] > 0:
            return BIKES_SHEET.get_image(0, 15 * PLAYER_WIDTH, 2 * PLAYER_WIDTH, PLAYER_WIDTH)
        elif dir[0] < 0:
            return BIKES_SHEET.get_image(0, 14 * PLAYER_WIDTH, 2 * PLAYER_WIDTH, PLAYER_WIDTH)
        else:
            if dir[1] > 0:
                return BIKES_SHEET.get_image(0, 6 * PLAYER_WIDTH, PLAYER_WIDTH, 2 * PLAYER_WIDTH)
            else:
                return BIKES_SHEET.get_image(PLAYER_WIDTH, 6 * PLAYER_WIDTH, PLAYER_WIDTH, 2 * PLAYER_WIDTH)
    elif (color == "GREEN"):
        if dir[0] > 0:
            return BIKES_SHEET.get_image(0, 11 * PLAYER_WIDTH, 2 * PLAYER_WIDTH, PLAYER_WIDTH)
        elif dir[0] < 0:
            return BIKES_SHEET.get_image(0, 10 * PLAYER_WIDTH, 2 * PLAYER_WIDTH, PLAYER_WIDTH)
        else:
            if dir[1] > 0:
                return BIKES_SHEET.get_image(0, 2 * PLAYER_WIDTH, PLAYER_WIDTH, 2 * PLAYER_WIDTH)
            else:
                return BIKES_SHEET.get_image(PLAYER_WIDTH, 2 * PLAYER_WIDTH, PLAYER_WIDTH, 2 * PLAYER_WIDTH)
    else:
        return getPowerupBike(dir, color)

def getPowerupBike(dir, color):
    if (color == "POWERUP_RED"):
        if dir[0] > 0:
            return POWERUP_BIKES_SHEET.get_image(0, 13 * PLAYER_WIDTH, 2 * PLAYER_WIDTH, PLAYER_WIDTH)
        elif dir[0] < 0:
            return POWERUP_BIKES_SHEET.get_image(0, 12 * PLAYER_WIDTH, 2 * PLAYER_WIDTH, PLAYER_WIDTH)
        else:
            if dir[1] > 0:
                return POWERUP_BIKES_SHEET.get_image(0, 4 * PLAYER_WIDTH, PLAYER_WIDTH, 2 * PLAYER_WIDTH)
            else:
                return POWERUP_BIKES_SHEET.get_image(PLAYER_WIDTH, 4 * PLAYER_WIDTH, PLAYER_WIDTH, 2 * PLAYER_WIDTH)
    elif (color == "POWERUP_BLUE"):
        if dir[0] > 0:
            return POWERUP_BIKES_SHEET.get_image(0, 9 * PLAYER_WIDTH, 2 * PLAYER_WIDTH, PLAYER_WIDTH)
        elif dir[0] < 0:
            return POWERUP_BIKES_SHEET.get_image(0, 8 * PLAYER_WIDTH, 2 * PLAYER_WIDTH, PLAYER_WIDTH)
        else:
            if dir[1] > 0:
                return POWERUP_BIKES_SHEET.get_image(0, 0, PLAYER_WIDTH, 2 * PLAYER_WIDTH)
            else:
                return POWERUP_BIKES_SHEET.get_image(PLAYER_WIDTH, 0, PLAYER_WIDTH, 2 * PLAYER_WIDTH)
    elif (color == "POWERUP_YELLOW"):
        if dir[0] > 0:
            return POWERUP_BIKES_SHEET.get_image(0, 15 * PLAYER_WIDTH, 2 * PLAYER_WIDTH, PLAYER_WIDTH)
        elif dir[0] < 0:
            return POWERUP_BIKES_SHEET.get_image(0, 14 * PLAYER_WIDTH, 2 * PLAYER_WIDTH, PLAYER_WIDTH)
        else:
            if dir[1] > 0:
                return POWERUP_BIKES_SHEET.get_image(0, 6 * PLAYER_WIDTH, PLAYER_WIDTH, 2 * PLAYER_WIDTH)
            else:
                return POWERUP_BIKES_SHEET.get_image(PLAYER_WIDTH, 6 * PLAYER_WIDTH, PLAYER_WIDTH, 2 * PLAYER_WIDTH)
    elif (color == "POWERUP_GREEN"):
        if dir[0] > 0:
            return POWERUP_BIKES_SHEET.get_image(0, 11 * PLAYER_WIDTH, 2 * PLAYER_WIDTH, PLAYER_WIDTH)
        elif dir[0] < 0:
            return POWERUP_BIKES_SHEET.get_image(0, 10 * PLAYER_WIDTH, 2 * PLAYER_WIDTH, PLAYER_WIDTH)
        else:
            if dir[1] > 0:
                return POWERUP_BIKES_SHEET.get_image(0, 2 * PLAYER_WIDTH, PLAYER_WIDTH, 2 * PLAYER_WIDTH)
            else:
                return POWERUP_BIKES_SHEET.get_image(PLAYER_WIDTH, 2 * PLAYER_WIDTH, PLAYER_WIDTH, 2 * PLAYER_WIDTH)

def getUnitVector(vector):
    return (sign(vector[0]), sign(vector[1]))




