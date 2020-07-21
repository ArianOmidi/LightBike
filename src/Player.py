import pygame
from Trail import *
from LightBike import *


class Player(pygame.sprite.Sprite):

    def __init__(self, color, start_pos, velocity):
        # Call parent class constructor
        super().__init__()

        self.color = color
        self.size = playerWidth
        self.lives = PLAYERLIVES

        self.powerup_active = False
        self.powerups_remaining = PLAYERLIVES
        self.speed = velocity

        self.init_velocity = velocity
        self.init_pos = start_pos

        self.image = pygame.image.load(getImages(self.color)[2 - sign(velocity)])
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]

        self.velocity = (self.speed, 0)
        self.activeTrail = None

        self.newTrail()

    def death(self):
        self.lives -= 1

        self.image = EXPLOSION
        self.rect.x -= 6
        self.rect.y -= 6

        if (self.lives == 0):
            return True

        return False

    def powerup(self):
        if self.speed == self.init_velocity:
            self.powerup_active = True
            self.powerup_time = POWERUPTIME * 60

            self.speed = int(self.init_velocity * SPEEDBOOSTFACTOR)
            self.setVelocity(self.velocity)

    def check_powerup(self):
        if (self.powerup_time > 0):
            self.powerup_time -= 1
        else:
            self.powerup_active = False
            self.speed = self.init_velocity

            self.setVelocity(self.velocity)

    def setVelocity(self, velocity):
        """ Change the speed of the player"""
        self.setImage(velocity)
        self.velocity = (sign(velocity[0]) * self.speed, sign(velocity[1]) * self.speed)
        self.newTrail()

    def newTrail(self):
        if self.activeTrail != None:
            self.activeTrail.endTrail()
        self.lastActiveTrail = self.activeTrail
        self.activeTrail = Trail(self, getTrailColor(self.color, self.powerup_active), (self.rect.x, self.rect.y), trailSize)

    def setImage(self, new_vel):
        if (new_vel[0] != 0):
            if (new_vel[0] < 0):
                self.image = pygame.image.load(getImages(self.color)[3])
                self.rect.x -= playerWidth
            else:
                self.image = pygame.image.load(getImages(self.color)[1])

            if (self.velocity[1] > 0):
                self.rect.y += playerWidth
        else:
            if (new_vel[1] < 0):
                self.image = pygame.image.load(getImages(self.color)[0])
                self.rect.y -= playerWidth
            else:
                self.image = pygame.image.load(getImages(self.color)[2])

            if (self.velocity[0] > 0):
                self.rect.x += playerWidth

        self.image.set_colorkey(WHITE)

    def reset(self):
        self.image = pygame.image.load(getImages(self.color)[2 - sign(self.init_velocity)])
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.init_pos[0]
        self.rect.y = self.init_pos[1]

        self.velocity = (self.init_velocity, 0)
        self.speed = self.init_velocity
        self.powerup_active = False

        self.newTrail()
        self.lastActiveTrail = None

    def update(self):
        """ Find a new position for the player"""
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        self.activeTrail.update()

        if self.powerup_active:
            self.check_powerup()


