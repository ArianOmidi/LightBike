import pygame
from Util import *

class Trail(pygame.sprite.Sprite):
    """ This class represents a simple block the player collects. """
    def __init__(self, player, color, start_pos, size):
        """ Constructor, create the image of the block. """
        super().__init__()
        self.player = player
        self.color = color
        self.size = size
        self.dir = player.velocity

        self.is_powerup_trail = self.player.powerup_active

        self.centering_factor = player.size / 2 - size / 2

        self.image = pygame.Surface([hasValue(self.dir[1]) * size, hasValue(self.dir[0]) * size])
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self. setStartPos(start_pos)

    def setStartPos(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        if (self.dir[0] > 0):
            self.rect.x += self.centering_factor
            self.rect.y += self.centering_factor
        elif (self.dir[0] < 0):
            self.rect.x += 2 * self.player.size  - self.centering_factor
            self.rect.y += self.centering_factor
        elif (self.dir[1] > 0):
            self.rect.x += self.centering_factor
            self.rect.y += self.centering_factor
        elif (self.dir[1] < 0):
            self.rect.x += self.centering_factor
            self.rect.y += 2 * self.player.size - self.centering_factor

    def endTrail(self):
        extendX = hasValue(self.dir[0]) * self.player.size
        extendY = hasValue(self.dir[1]) * self.player.size

        old_pos = (self.rect.x, self.rect.y)

        self.image = pygame.Surface((self.image.get_width() + extendX, self.image.get_height() + extendY))
        self.image.fill(self.color)

        self.add_boost_stripe()

        self.rect = self.image.get_rect()
        self.rect.x = old_pos[0]
        self.rect.y = old_pos[1]

        if (self.dir[0] < 0 or self.dir[1] < 0):
            self.rect.x -= extendX
            self.rect.y -= extendY

    def update(self):
        """ Automatically called when we need to move the block. """
        old_pos = (self.rect.x, self.rect.y)

        self.image = pygame.Surface((self.image.get_width() + abs(self.dir[0]), self.image.get_height() + abs(self.dir[1])))
        self.image.fill(self.color)

        self.add_boost_stripe()


        self.rect = self.image.get_rect()
        self.rect.x = old_pos[0]
        self.rect.y = old_pos[1]


        if (self.dir[0] < 0 or self.dir[1] < 0):
            self.rect.x += self.dir[0]
            self.rect.y += self.dir[1]

    def add_boost_stripe(self):
        if (self.is_powerup_trail):
            vel = self.dir
            # divider = 3
            # num_of_dots = int((self.image.get_width() * hasValue(self.dir[0]) + self.image.get_height() * hasValue(self.dir[1])) / trailSize / divider)
            #
            # for i in range(0, num_of_dots + 1):
            #     dot = pygame.Surface((trailSize, trailSize))
            #     dot.fill(BLACK)
            #
            #     self.image.blit(dot, (divider * trailSize * i * hasValue(self.dir[0]), divider * trailSize * i * hasValue(self.dir[1])))
        else:
            stripe = pygame.Surface((self.image.get_width() - 2, self.image.get_height() - 2))
            stripe.fill(BLACK)

            self.image.blit(stripe, (1, 1))


