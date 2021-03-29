from PIL import Image
from pygame import Surface
from pygame import font
from pygame import image
from pygame import init

from SoundPlayer import SoundPlayer

init()

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
TEXT_COLOR = (230, 230, 230)
DARK_TEXT_COLOR = (97, 97, 97)

# --- TRAIL COLORS --- #
RED = (232, 12, 12)
TRAILRED = (191, 19, 19)
BOOSTREDTRAIL = (237, 60, 47)
YELLOW = (255, 247, 0)
GREEN = (0, 255, 0)
BLUE = (117, 164, 255)

# --- DESIGN VARIABLES --- #
BORDER_WIDTH = 5
GRIDLINES = 10

""" --- PLAYER VARIABLES --- """

PLAYER_WIDTH = 11
TRAIL_SIZE = 3
PLAYER_LIVES = 3
VELOCITY = 3

# --- BOOSTER --- #
BOOST_TRAIL_DIVIDER = 3
SPEED_BOOST_FACTOR = 2
BOOSTER_POWERUP_TIME = 3.5
BOOSTER_POWERUP_NUM = 3

# --- JUMPER --- #
JUMP_TIME = 0.5
JUMPER_POWERUP_TIME = 4
JUMPER_POWERUP_NUM = 3

# --- GHOST --- #
INVISIBLE_POWERUP_TIME = 2.5
INVISIBLE_POWERUP_NUM = 3

# --- BUILDER --- #
BUILDER_POWERUP_TIME = 2
WALL_SPEED_FACTOR = 1.5
BUILDER_POWERUP_NUM = 4

""" --- GAME VARIABLES --- """
FPS = 40
SCREEN_HEIGHT = 750
SCREEN_WIDTH = 1400
BORDER_TOP_OFFSET = 55
PLAYER_ONE_STARTING_POS = (SCREEN_WIDTH * 1 / 10, (SCREEN_HEIGHT + BORDER_TOP_OFFSET - PLAYER_WIDTH) / 5)
PLAYER_TWO_STARTING_POS = (
SCREEN_WIDTH * 9 / 10 - 2 * PLAYER_WIDTH, (SCREEN_HEIGHT + BORDER_TOP_OFFSET - PLAYER_WIDTH) * 4 / 5)
NUM_OF_PLAYERS = 2

PLAYER_SELECT_OFFSET = 25
PLAYER_SELECT_BORDER = 10

POWERUP_SELECTION_ICON_SIZE = 150

""" --- IMAGES --- """

EXPLOSION = image.load("resources/images/explosions/explosion.png")

HEART = image.load("resources/images/icons/heart.png")
EMPTY_HEART = image.load("resources/images/icons/empty_heart.png")
POWERUP_ICON = image.load("resources/images/icons/powerup_icon.png")
EMPTY_POWERUP_ICON = image.load("resources/images/icons/empty_powerup_icon.png")

BIKES_SHEET = SpriteSheet("resources/images/sprite_sheets/bikes_sprite_sheet.png")
POWERUP_BIKES_SHEET = SpriteSheet("resources/images/sprite_sheets/bikes_sprite_sheet_powerup.png")
ICON_BIKES_SHEET = SpriteSheet("resources/images/sprite_sheets/icon_bikes_sprite_sheet.png")
PLAYER_SELECTION_BIKE_SHEET = SpriteSheet("resources/images/sprite_sheets/player_select_bike_sheet.png")
POWERUP_SELECTION_SHEET = SpriteSheet("resources/images/sprite_sheets/powerup_sheet.png")

INTRO_SCREEN = image.load("resources/images/backgrounds/intro_screen.png")
PLAYER_SELECT_SCREEN = image.load("resources/images/backgrounds/empty_menu_screen.png")
INSTRUCTION_SCREEN = image.load("resources/images/backgrounds/instruction_screen.png")

SOUND_PLAYER = SoundPlayer()


# --- INIT FONTS --- # (Reduces lag)

def init_fonts(game):
    global LOGO_ICON, P1_TEXT, P2_TEXT, GAME_OVER_TEXT, P1_WINS_TEXT, P2_WINS_TEXT, CONTINUE_TEXT, DRAW_TEXT

    LOGO_ICON = []
    P1_TEXT = []
    P2_TEXT = []
    GAME_OVER_TEXT = []
    P1_WINS_TEXT = []
    P2_WINS_TEXT = []
    DRAW_TEXT = []
    CONTINUE_TEXT = []

    fontObj = font.Font("resources/fonts/retronoid.ttf", 50)

    LOGO_ICON.append(fontObj.render("Light Bike", True, TEXT_COLOR))
    LOGO_ICON.append(LOGO_ICON[0].get_rect())
    LOGO_ICON[1].center = (SCREEN_WIDTH // 2, (BORDER_TOP_OFFSET) // 2)

    LOGO_ICON.append(fontObj.render("Light Bike", True, DARK_TEXT_COLOR))

    fontObj = font.Font("resources/fonts/retronoid.ttf", 40)

    P1_TEXT.append(fontObj.render("P1", True, TEXT_COLOR))
    P1_TEXT.append(P1_TEXT[0].get_rect())
    P1_TEXT[1].center = (40, BORDER_TOP_OFFSET // 2)

    P2_TEXT.append(fontObj.render("P2", True, TEXT_COLOR))
    P2_TEXT.append(P2_TEXT[0].get_rect())
    P2_TEXT[1].center = (SCREEN_WIDTH - 40, BORDER_TOP_OFFSET // 2)

    fontObj = font.Font("resources/fonts/retronoid.ttf", 100)

    GAME_OVER_TEXT.append(fontObj.render("Game Over", True, TEXT_COLOR))
    GAME_OVER_TEXT.append(GAME_OVER_TEXT[0].get_rect())
    GAME_OVER_TEXT[1].center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    fontObj = font.Font("resources/fonts/retronoid.ttf", 50)

    P1_WINS_TEXT.append(fontObj.render("Player 1 Wins", True, getTrailColor(game.player_one.color, None)))
    P1_WINS_TEXT.append(P1_WINS_TEXT[0].get_rect())
    P1_WINS_TEXT[1].center = (
    SCREEN_WIDTH // 2, (SCREEN_HEIGHT - P1_WINS_TEXT[0].get_height()) // 2 + GAME_OVER_TEXT[0].get_height())

    if hasattr(game, "player_two"):
        P2_WINS_TEXT.append(fontObj.render("Player 2 Wins", True, getTrailColor(game.player_two.color, None)))
        P2_WINS_TEXT.append(P1_WINS_TEXT[1])

    DRAW_TEXT.append(fontObj.render("DRAW", True, TEXT_COLOR))
    DRAW_TEXT.append(DRAW_TEXT[0].get_rect())
    DRAW_TEXT[1].center = (
        SCREEN_WIDTH // 2, (SCREEN_HEIGHT - DRAW_TEXT[0].get_height()) // 2 + GAME_OVER_TEXT[0].get_height())

    fontObj = font.Font("resources/fonts/retronoid.ttf", 20)

    CONTINUE_TEXT.append(fontObj.render("Press Enter To Exit To Bike Selection", True, TEXT_COLOR))
    CONTINUE_TEXT.append((SCREEN_WIDTH - 2 * BORDER_WIDTH - CONTINUE_TEXT[0].get_width(),
                          SCREEN_HEIGHT - BORDER_WIDTH - CONTINUE_TEXT[0].get_height()))

    CONTINUE_TEXT.append(fontObj.render("Press R To Replay", True, TEXT_COLOR))
    CONTINUE_TEXT.append((SCREEN_WIDTH - 2 * BORDER_WIDTH - CONTINUE_TEXT[2].get_width(),
                          SCREEN_HEIGHT - BORDER_WIDTH - CONTINUE_TEXT[0].get_height() - CONTINUE_TEXT[2].get_height()))


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
        return RED
    elif (color == "YELLOW"):
        return YELLOW
    elif (color == "BLUE"):
        return BLUE
    elif (color == "GREEN"):
        return GREEN


def getNumOfPowerups(type):
    if (type == "BOOSTER"):
        return BOOSTER_POWERUP_NUM
    elif (type == "BUILDER"):
        return BUILDER_POWERUP_NUM
    elif (type == "GHOST"):
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


def getPlayerSelectionBike(color, player):
    if (color == "RED"):
        if player == 1:
            return PLAYER_SELECTION_BIKE_SHEET.get_image(4 * 20 * PLAYER_WIDTH, 0, 20 * PLAYER_WIDTH, 10 * PLAYER_WIDTH)
        elif player == 2:
            return PLAYER_SELECTION_BIKE_SHEET.get_image(5 * 20 * PLAYER_WIDTH, 0, 20 * PLAYER_WIDTH, 10 * PLAYER_WIDTH)
    elif (color == "BLUE"):
        if player == 1:
            return PLAYER_SELECTION_BIKE_SHEET.get_image(0, 0, 20 * PLAYER_WIDTH, 10 * PLAYER_WIDTH)
        elif player == 2:
            return PLAYER_SELECTION_BIKE_SHEET.get_image(20 * PLAYER_WIDTH, 0, 20 * PLAYER_WIDTH, 10 * PLAYER_WIDTH)
    elif (color == "YELLOW"):
        if player == 1:
            return PLAYER_SELECTION_BIKE_SHEET.get_image(6 * 20 * PLAYER_WIDTH, 0, 20 * PLAYER_WIDTH, 10 * PLAYER_WIDTH)
        elif player == 2:
            return PLAYER_SELECTION_BIKE_SHEET.get_image(7 * 20 * PLAYER_WIDTH, 0, 20 * PLAYER_WIDTH, 10 * PLAYER_WIDTH)
    elif (color == "GREEN"):
        if player == 1:
            return PLAYER_SELECTION_BIKE_SHEET.get_image(2 * 20 * PLAYER_WIDTH, 0, 20 * PLAYER_WIDTH, 10 * PLAYER_WIDTH)
        elif player == 2:
            return PLAYER_SELECTION_BIKE_SHEET.get_image(3 * 20 * PLAYER_WIDTH, 0, 20 * PLAYER_WIDTH, 10 * PLAYER_WIDTH)


def getPowerupSelectionIcon(powerup):
    if powerup == "BOOST":
        return POWERUP_SELECTION_SHEET.get_image(0, 0, 150, 150)
    elif powerup == "GHOST":
        return POWERUP_SELECTION_SHEET.get_image(1 * 150, 0, 150, 150)
    elif powerup == "JUMP":
        return POWERUP_SELECTION_SHEET.get_image(2 * 150, 0, 150, 150)
    elif powerup == "WALL":
        return POWERUP_SELECTION_SHEET.get_image(3 * 150, 0, 150, 150)
    else:
        return PLAYER_SELECTION_BIKE_SHEET.get_image(3 * 20 * PLAYER_WIDTH, 0, 20 * PLAYER_WIDTH, 10 * PLAYER_WIDTH)

def getUnitVector(vector):
    return (sign(vector[0]), sign(vector[1]))


def getColorIndex(color):
    if (color == "RED"):
        return 0
    elif (color == "BLUE"):
        return 1
    elif (color == "YELLOW"):
        return 2
    elif (color == "GREEN"):
        return 3
    else:
        return -1


def getColor(index):
    if (index == 0):
        return "RED"
    elif (index == 1):
        return "BLUE"
    elif (index == 2):
        return "YELLOW"
    elif (index == 3):
        return "GREEN"
    else:
        return ""


def getPowerupIndex(powerup):
    if (powerup == "WALL"):
        return 0
    elif (powerup == "GHOST"):
        return 1
    elif (powerup == "BOOST"):
        return 2
    elif (powerup == "JUMP"):
        return 3
    else:
        return -1


def getPowerup(index):
    if (index == 0):
        return "WALL"
    elif (index == 1):
        return "GHOST"
    elif (index == 2):
        return "BOOST"
    elif (index == 3):
        return "JUMP"
    else:
        return ""


def getPowerupColor(index):
    if (index == 0):
        return (234, 203, 78)
    elif (index == 1):
        return (179, 188, 214)
    elif (index == 2):
        return (116, 156, 71)
    elif (index == 3):
        return (155, 56, 45)
    else:
        return WHITE



def blit_text(text, font_style, size, color, center, screen):
    fontObj = font.Font("resources/fonts/" + font_style + ".ttf", size)
    textObj = fontObj.render(text, True, color)

    textRect = textObj.get_rect()
    textRect.center = center

    screen.blit(textObj, textRect)


def blit_icon_bar(screen):
    screen.blit(LOGO_ICON[0], LOGO_ICON[1])
    screen.blit(P1_TEXT[0], P1_TEXT[1])
    screen.blit(P2_TEXT[0], P2_TEXT[1])



def gameover_text(game, screen):
    screen.blit(GAME_OVER_TEXT[0], GAME_OVER_TEXT[1])
    screen.blit(CONTINUE_TEXT[0], CONTINUE_TEXT[1])
    screen.blit(CONTINUE_TEXT[2], CONTINUE_TEXT[3])

    if game.player_one.lives == 0:
        if not game.player_two.lives == 0:
            screen.blit(P2_WINS_TEXT[0], P2_WINS_TEXT[1])
        else:
            screen.blit(DRAW_TEXT[0], DRAW_TEXT[1])
    else:
        screen.blit(P1_WINS_TEXT[0], P1_WINS_TEXT[1])
