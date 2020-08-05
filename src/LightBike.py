import pygame
import random
from time import sleep
from Player import *
from Trail import *
from Util import *

SCREEN_HEIGHT = 700
SCREEN_WIDTH = 1400

PLAYER_SIZE = 11
PLAYER_ONE_STARTING_POS = (0, (SCREEN_HEIGHT - PLAYER_SIZE) / 2)
PLAYER_TWO_STARTING_POS = (SCREEN_WIDTH - 2 * PLAYER_SIZE, (SCREEN_HEIGHT - PLAYER_SIZE) / 2)
VELOCITY = 2

class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """

    def __init__(self):
        """ Constructor. Create all our attributes and initialize
        the game. """

        self.score = 0
        self.counter = 0
        self.game_over = False
        self.round_in_progress = False

        # Create sprite lists
        self.trail_list = pygame.sprite.Group()
        self.player_list = pygame.sprite.Group()

        # Create the player
        self.player_one = Booster("RED", PLAYER_TWO_STARTING_POS, -VELOCITY)
        # self.player_two = Invisible("YELLOW", PLAYER_TWO_STARTING_POS, -VELOCITY)

        self.player_list.add(self.player_one)
        # self.player_list.add(self.player_two)

    # def addTrail(self, player):
    #     if (self.trail_list.__contains__(player.activeTrail) == False):
    #         self.trail_list.add(self.player.activeTrail)

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    self.__init__()

            if event.type == pygame.KEYDOWN:
                # Player One
                if (self.player_one.velocity[0] == 0):
                    if event.key == pygame.K_LEFT:
                            self.player_one.setVelocity((-VELOCITY, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.player_one.setVelocity((VELOCITY, 0))
                else:
                    if event.key == pygame.K_UP:
                        self.player_one.setVelocity((0, -VELOCITY))
                    elif event.key == pygame.K_DOWN:
                        self.player_one.setVelocity((0, VELOCITY))

                if event.key == pygame.K_SPACE:
                    self.player_one.powerup()

                # Player Two

                # if (self.player_two.velocity[0] == 0):
                #     if event.key == pygame.K_a:
                #             self.player_two.setVelocity((-VELOCITY, 0))
                #     elif event.key == pygame.K_d:
                #         self.player_two.setVelocity((VELOCITY, 0))
                # else:
                #     if event.key == pygame.K_w:
                #         self.player_two.setVelocity((0, -VELOCITY))
                #     elif event.key == pygame.K_s:
                #         self.player_two.setVelocity((0, VELOCITY))
                #
                # if event.key == pygame.K_RETURN:
                #     self.player_two.powerup()

        return False

    def new_round(self, screen):
        self.counter += 1

        # if (self.counter < 60):
        #     screen.blit(ONE, (0,0))
        #     return
        # elif (self.counter < 120):
        #     screen.blit(TWO, (0, 0))
        #     return
        # elif (self.counter < 180):
        #     screen.blit(THREE, (0, 0))
        #     return

        self.trail_list.empty()

        for player in self.player_list:
            player.reset()
            self.trail_list.add(player.activeTrail)

        self.round_in_progress = True
        self.counter = 0


    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        if self.game_over == False and self.round_in_progress:
            # Move the player
            self.player_list.update()

            for player in self.player_list:

                if not (self.trail_list.__contains__(player.activeTrail) or player.activeTrail is None) :
                    self.trail_list.add(player.activeTrail)

                # If player invulnerable skip over hit detection
                if player.invulnerable:
                    continue

                # See if the player has collided with anything.
                trail_hit_list = pygame.sprite.spritecollide(player, self.trail_list, False)

                # Check the list of collisions.
                for trail in trail_hit_list:
                    if (trail == player.activeTrail or trail == player.lastActiveTrail):
                        continue

                    self.score += 1
                    print(self.score)

                    self.game_over = player.death()
                    self.round_in_progress = False
                    break
                    # You can do something with "block" here.

    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        self.clear_screen(screen)

        if self.game_over:
            # font = pygame.font.Font("Serif", 25)
            font = pygame.font.SysFont("serif", 25)
            text = font.render("Game Over, click to restart", True, WHITE)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])
        elif self.round_in_progress == False:
            self.new_round(screen)

        self.trail_list.draw(screen)
        self.player_list.draw(screen)

        pygame.display.update()

    def clear_screen(self, screen):
        screen.fill(BACKGROUND)

        for i in range(0, GRIDLINES):
            pygame.draw.line(screen, GRIDCOLOR, [0, i * SCREEN_WIDTH / GRIDLINES + SCREEN_WIDTH / GRIDLINES / 2], [SCREEN_WIDTH, i * SCREEN_WIDTH / GRIDLINES + SCREEN_WIDTH / GRIDLINES / 2], 1)
        for j in range(0, GRIDLINES):
            pygame.draw.line(screen, GRIDCOLOR, [j * SCREEN_WIDTH / GRIDLINES + SCREEN_WIDTH / GRIDLINES / 2, 0], [j * SCREEN_WIDTH / GRIDLINES + SCREEN_WIDTH / GRIDLINES / 2, SCREEN_WIDTH], 1)

        for i in range(0, GRIDLINES + 1):
            pygame.draw.line(screen, BACKGROUND, [0, i * SCREEN_WIDTH / GRIDLINES ], [SCREEN_WIDTH, i * SCREEN_WIDTH / GRIDLINES ], int(SCREEN_WIDTH / GRIDLINES / 6))
        for j in range(0, GRIDLINES + 1):
            pygame.draw.line(screen, BACKGROUND, [j * SCREEN_WIDTH / GRIDLINES , 0],
                             [j * SCREEN_WIDTH / GRIDLINES , SCREEN_WIDTH], int(SCREEN_WIDTH / GRIDLINES / 6))

def main():
    """ Main program function. """
    # Initialize Pygame and set up the window
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Light Bike")
    pygame.mouse.set_visible(True)

    # Create our objects and set the data
    done = False
    clock = pygame.time.Clock()

    # Create an instance of the Game class
    game = Game()

    # Main game loop
    while not done:
        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()

        # Update object positions, check for collisions
        game.run_logic()

        # Draw the current frame
        game.display_frame(screen)

        # Pause for the next frame
        clock.tick(FPS)

    # Close window and exit
    pygame.quit()


# Call the main function, start up the game
if __name__ == "__main__":
    main()