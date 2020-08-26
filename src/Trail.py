from Util import *
import pygame


class Trail(pygame.sprite.Sprite):
    """ This class represents a simple block the player collects. """

    def __init__(self, player, color, start_pos):
        super().__init__()

        # Variables
        self.color = color
        self.size = TRAIL_SIZE
        self.dir = player.velocity

        self.image = pygame.Surface([hasValue(self.dir[1]) * self.size, hasValue(self.dir[0]) * self.size])
        self.image.fill(self.color)

        # Set start position
        self.rect = self.image.get_rect()
        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]

        self.centering_factor = PLAYER_WIDTH / 2 - self.size / 2

        if (self.dir[0] > 0):
            self.rect.x += self.centering_factor
            self.rect.y += self.centering_factor
        elif (self.dir[0] < 0):
            self.rect.x += 2 * PLAYER_WIDTH - self.centering_factor
            self.rect.y += self.centering_factor
        elif (self.dir[1] > 0):
            self.rect.x += self.centering_factor
            self.rect.y += self.centering_factor
        elif (self.dir[1] < 0):
            self.rect.x += self.centering_factor
            self.rect.y += 2 * PLAYER_WIDTH - self.centering_factor


    def endTrail(self):
        extendX = hasValue(self.dir[0]) * PLAYER_WIDTH
        extendY = hasValue(self.dir[1]) * PLAYER_WIDTH

        old_pos = (self.rect.x, self.rect.y)

        self.image = pygame.Surface((self.image.get_width() + extendX, self.image.get_height() + extendY))
        self.add_design()

        self.rect = self.image.get_rect()
        self.rect.x = old_pos[0]
        self.rect.y = old_pos[1]

        if (self.dir[0] < 0 or self.dir[1] < 0):
            self.rect.x -= extendX
            self.rect.y -= extendY

    def update(self):
        old_pos = (self.rect.x, self.rect.y)

        self.image = pygame.Surface((self.image.get_width() + abs(self.dir[0]), self.image.get_height() + abs(self.dir[1])))
        self.add_design()

        self.rect = self.image.get_rect()
        self.rect.x = old_pos[0]
        self.rect.y = old_pos[1]


        if (self.dir[0] < 0 or self.dir[1] < 0):
            self.rect.x += self.dir[0]
            self.rect.y += self.dir[1]

    def add_design(self):
        self.image.fill(self.color)

        if (self.image.get_width() >= 2 and self.image.get_height() >= 2):
            stripe = pygame.Surface((self.image.get_width() - 2, self.image.get_height() - 2))
            stripe.fill(BACKGROUND)
            self.image.blit(stripe, (1, 1))


# --- BOOST TRAIL --- #

class BoostTrail(Trail):
    def __init__(self, player, color, start_pos):
        super().__init__(player, color, start_pos)

    def add_design(self):
        super().add_design()

        num_of_dots = ceil((self.image.get_width() * hasValue(self.dir[0]) + self.image.get_height() * hasValue(
            self.dir[1])) // BOOST_TRAIL_DIVIDER)

        for i in range(0, num_of_dots):
            dot = pygame.Surface((self.size, self.size))
            dot.fill(BACKGROUND)

            if (self.dir[0] > 0 or self.dir[1] > 0):
                self.image.blit(dot, (
                    BOOST_TRAIL_DIVIDER * self.size * i * hasValue(self.dir[0]),
                    BOOST_TRAIL_DIVIDER * self.size * i * hasValue(self.dir[1])))
            else:
                self.image.blit(dot, (
                    (self.image.get_width() - BOOST_TRAIL_DIVIDER * self.size * (i + 1)) * hasValue(self.dir[0]),
                    (self.image.get_height() - BOOST_TRAIL_DIVIDER * self.size * (i + 1)) * hasValue(self.dir[1])))


# --- WALL TRAIL --- #

class Wall(Trail):
    def __init__(self, player, color, start_pos, old_trail):
        super().__init__(player, color, start_pos)

        wall_pos = (self.rect.x, self.rect.y)

        self.image = pygame.Surface((self.image.get_width() + hasValue(self.dir[0]) * (old_trail.image.get_width()),
                                     self.image.get_height() + hasValue(self.dir[1]) * (old_trail.image.get_height())))
        self.add_design()

        self.rect = self.image.get_rect()

        if (old_trail.dir[0] > 0 or old_trail.dir[1] > 0):
            self.rect.x = old_trail.rect.x
            self.rect.y = old_trail.rect.y
        else:
            self.rect.x = wall_pos[0]
            self.rect.y = wall_pos[1]

        self.dir = (self.dir[0] * WALL_SPEED_FACTOR, self.dir[1] * WALL_SPEED_FACTOR)

    # Return false if out of bounds
    def update(self):
        if not (self.rect.x + self.dir[0] < BORDER_WIDTH or self.rect.y + self.dir[
            1] < BORDER_TOP_OFFSET + BORDER_WIDTH or self.image.get_height() + self.rect.y + self.dir[
                    1] > SCREEN_HEIGHT - BORDER_WIDTH or self.image.get_width() + self.rect.x + self.dir[
                    0] > SCREEN_WIDTH - BORDER_WIDTH):
            super().update()

            return True

        return False

    def endTrail(self):
        return None



