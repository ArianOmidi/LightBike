from pygame import image

""" --- GRAPHIC CONSTANTS --- """

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

EXPLOISION_PATH = "resources/images/explosions/explosion.png"

HEART_PATH = "resources/images/icons/heart.png"
EMPTY_HEART_PATH = "resources/images/icons/empty_heart.png"
POWERUP_ICON_PATH = "resources/images/icons/powerup_icon.png"
EMPTY_POWERUP_ICON_PATH = "resources/images/icons/empty_powerup_icon.png"

BIKES_SHEET_PATH = "resources/images/sprite_sheets/bikes_sprite_sheet.png"
POWERUP_BIKES_SHEET_PATH = "resources/images/sprite_sheets/bikes_sprite_sheet_powerup.png"
ICON_BIKES_SHEET_PATH = "resources/images/sprite_sheets/icon_bikes_sprite_sheet.png"
PLAYER_SELECTION_BIKE_SHEET_PATH = "resources/images/sprite_sheets/player_select_bike_sheet.png"
POWERUP_SELECTION_SHEET_PATH = "resources/images/sprite_sheets/powerup_sheet.png"

INTRO_SCREEN_PATH = "resources/images/backgrounds/intro_screen.png"
PLAYER_SELECT_SCREEN_PATH = "resources/images/backgrounds/empty_menu_screen.png"
INSTRUCTION_SCREEN_PATH = "resources/images/backgrounds/instruction_screen.png"


""" --- AUDIO --- """

THEME_SONG = "resources/audio/lightbike_theme_song.wav"

MENU_HIGHLIGHT_AUDIO = "resources/audio/menu_select.wav"
MENU_ACTION_AUDIO  = "resources/audio/menu_validate.wav"
MENU_CONTINUE_AUDIO = "resources/audio/menu_continue.wav"

ROUND_START_AUDIO = "resources/audio/round_start.wav"
ROUND_RESET_AUDIO = "resources/audio/round_reset.wav"
GAME_OVER_AUDIO = "resources/audio/game_over.wav"
CRASH_AUDIO = "resources/audio/crash.wav"

BOOST_AUDIO = "resources/audio/boost.wav"
JUMP_AUDIO = "resources/audio/jump.wav"
GHOST_AUDIO = "resources/audio/ghost.wav"
WALL_AUDIO = "resources/audio/wall.wav"

""" --- FONTS --- """

RETRONOID_FONT = "resources/fonts/retronoid.ttf"

