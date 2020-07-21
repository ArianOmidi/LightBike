import pygame
from Trail import *
from LightBike import *
trailSize = 8

class Player(pygame.sprite.Sprite):

    def __init__(self, color, start_x, start_y, velocity, size):
        # Call parent class constructor
        super().__init__()

        self.color = color
        self.size = size

        self.image = pygame.Surface([2 * size, size])
        self.image.fill(color)
        # self.image.fill(WHITE)
        # self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y

        self.velocity = (velocity, 0)

        self.activeTrail = Trail(self, (start_x, start_y), trailSize)


    def setVelocity(self, velocity):
        """ Change the speed of the player"""
        self.setOrientation(velocity)
        self.velocity = velocity
        self.newTrail()

    def newTrail(self):
        self.activeTrail.endTrail()
        self.lastActiveTrail = self.activeTrail
        self.activeTrail = Trail(self, (self.rect.x, self.rect.y), trailSize)

    def setOrientation(self, new_vel):
        if (new_vel[0] != 0):
            self.image = pygame.Surface([2 * self.size, self.size])

            if (new_vel[0] < 0):
                self.rect.x -= self.size
            if (self.velocity[1] > 0):
                self.rect.y += self.size

        else:
            self.image = pygame.Surface([self.size, 2 * self.size])

            if (new_vel[1] < 0):
                self.rect.y -= self.size
            if (self.velocity[0] > 0):
                self.rect.x += self.size

        self.image.fill(self.color)

    def update(self):
        """ Find a new position for the player"""
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        self.activeTrail.update()

        # old_pos = (self.rect.x, self.rect.y)
        #
        #
        # self.image = pygame.Surface((self.image.get_width() + self.velocity[0], self.image.get_height() + self.velocity[1]))
        # self.image.fill(self.color)
        # self.rect = self.image.get_rect()
        # self.rect.x = old_pos[0]
        # self.rect.y = old_pos[1]



