import pygame
import random
from Player import *
from Trail import *
from Util import *

SCREEN_HEIGHT = 700
SCREEN_WIDTH = 700

PLAYER_SIZE = 11
PLAYER_STARTING_POS = (0, (SCREEN_HEIGHT - PLAYER_SIZE) / 2)
VELOCITY = 2

class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """

    def __init__(self):
        """ Constructor. Create all our attributes and initialize
        the game. """

        self.score = 0
        self.game_over = False

        # Create sprite lists
        self.trail_list = pygame.sprite.Group()
        self.player_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()

        # Create the player
        self.player = Player(RED, PLAYER_STARTING_POS[0], PLAYER_STARTING_POS[1], VELOCITY, PLAYER_SIZE, TRAILRED)
        self.all_sprites_list.add(self.player)
        self.player_list.add(self.player)
        # TODO
        self.addTrail()

    def addTrail(self):
        if (self.all_sprites_list.__contains__(self.player.activeTrail) == False):
            self.all_sprites_list.add(self.player.activeTrail)
            self.trail_list.add(self.player.activeTrail)


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
                if event.key == pygame.K_LEFT:
                    self.player.setVelocity((-VELOCITY, 0))
                    self.addTrail()
                elif event.key == pygame.K_RIGHT:
                    self.player.setVelocity((VELOCITY, 0))
                    self.addTrail()
                elif event.key == pygame.K_UP:
                    self.player.setVelocity((0, -VELOCITY))
                    self.addTrail()
                elif event.key == pygame.K_DOWN:
                    self.player.setVelocity((0, VELOCITY))
                    self.addTrail()


        return False

    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        if not self.game_over:
            # Move all the sprites
            self.player_list.update()

            for player in self.player_list:
                # See if the player block has collided with anything.
                trail_hit_list = pygame.sprite.spritecollide(player, self.trail_list, False)

                # Check the list of collisions.
                for trail in trail_hit_list:
                    if (trail == player.activeTrail or trail == player.lastActiveTrail):
                        continue

                    self.score += 1
                    print(self.score)
                    # You can do something with "block" here.
                #
                # if len(self.block_list) == 0:
                #     self.game_over = True

    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        self.clear_screen(screen)

        if self.game_over:
            # font = pygame.font.Font("Serif", 25)
            font = pygame.font.SysFont("serif", 25)
            text = font.render("Game Over, click to restart", True, BLACK)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])

        if not self.game_over:
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

    pygame.display.set_caption("LightBike")
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
        clock.tick(60)

    # Close window and exit
    pygame.quit()


# Call the main function, start up the game
if __name__ == "__main__":
    main()