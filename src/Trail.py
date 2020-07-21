import pygame
from Util import *

class Trail(pygame.sprite.Sprite):
    """ This class represents a simple block the player collects. """
    def __init__(self, player, start_pos, size):
        """ Constructor, create the image of the block. """
        super().__init__()
        self.player = player
        self.color = player.trailColor
        self.size = size
        self.dir = player.velocity

        self.centering_factor = player.size / 2 - size / 2

        self.image = pygame.Surface([ hasValue(self.dir[1]) * size, hasValue(self.dir[0]) * size])
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
        extendX = hasValue(self.dir[0]) * (self.centering_factor + self.player.size)
        extendY = hasValue(self.dir[1]) * self.player.size

        old_pos = (self.rect.x, self.rect.y)

        self.image = pygame.Surface((self.image.get_width() + extendX, self.image.get_height() + extendY))
        self.image.fill(self.color)

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

        self.rect = self.image.get_rect()
        self.rect.x = old_pos[0]
        self.rect.y = old_pos[1]

        if (self.dir[0] < 0 or self.dir[1] < 0):
            self.rect.x += self.dir[0]
            self.rect.y += self.dir[1]



