import pygame
from Trail import *
from LightBike import *
trailSize = 3

class Player(pygame.sprite.Sprite):

    def __init__(self, color, start_x, start_y, velocity, size, trailColor):
        # Call parent class constructor
        super().__init__()

        self.color = color
        self.trailColor = trailColor
        self.size = size

        self.image = pygame.image.load("../resources/RedCarR.png")
        self.image.set_colorkey(WHITE)
        # self.image.fill(color)
        # self.image.fill(WHITE)
        # self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y

        self.velocity = (velocity, 0)

        self.activeTrail = Trail(self, (start_x, start_y), trailSize)


    def setVelocity(self, velocity):
        """ Change the speed of the player"""
        self.setImage(velocity)
        self.velocity = velocity
        self.newTrail()

    def newTrail(self):
        self.activeTrail.endTrail()
        self.lastActiveTrail = self.activeTrail
        self.activeTrail = Trail(self, (self.rect.x, self.rect.y), trailSize)

    def setImage(self, new_vel):
        if (new_vel[0] != 0):
            if (new_vel[0] < 0):
                self.image = pygame.image.load(getImages(self.color)[3])
                self.rect.x -= self.size
            else:
                self.image = pygame.image.load(getImages(self.color)[1])

            if (self.velocity[1] > 0):
                self.rect.y += self.size
        else:
            if (new_vel[1] < 0):
                self.image = pygame.image.load(getImages(self.color)[0])
                self.rect.y -= self.size
            else:
                self.image = pygame.image.load(getImages(self.color)[2])

            if (self.velocity[0] > 0):
                self.rect.x += self.size

        self.image.set_colorkey(WHITE)

    def update(self):
        """ Find a new position for the player"""
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        self.activeTrail.update()



