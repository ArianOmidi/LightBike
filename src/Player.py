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
        self.invulnerable = False

        self.init_velocity = velocity
        self.init_pos = start_pos

        self.image = pygame.image.load(getImages(self.color)[2 - sign(velocity)])
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]

        self.velocity = (velocity, 0)
        self.activeTrail = None

        self.newTrail()

    # --- Abstract Classes --- #

    # def powerup(self):

    # def check_powerup(self):

    # --- Setters --- #

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

    def setVelocity(self, velocity):
        """ Change the speed of the player"""
        self.setImage(velocity)
        self.velocity = velocity
        self.newTrail()

    def newTrail(self):
        if self.activeTrail != None:
            self.activeTrail.endTrail()
        self.lastActiveTrail = self.activeTrail
        self.activeTrail = Trail(self, getTrailColor(self.color, self.powerup_active), (self.rect.x, self.rect.y), trailSize)

    # --- Death Classes --- #
    def death(self):
        self.lives -= 1

        self.image = EXPLOSION
        self.rect.x -= 6
        self.rect.y -= 6

        if (self.lives == 0):
            return True

        return False

    def reset(self):
        self.powerup_active = False

        self.image = pygame.image.load(getImages(self.color)[2 - sign(self.init_velocity)])
        self.image.set_colorkey(WHITE)


        self.velocity = (self.init_velocity, 0)
        self.rect = self.image.get_rect()
        self.rect.x = self.init_pos[0]
        self.rect.y = self.init_pos[1]

        self.newTrail()
        self.lastActiveTrail = None



    def update(self):
        """ Find a new position for the player"""
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if (self.activeTrail is not None):
            self.activeTrail.update()

        if self.powerup_active:
            self.check_powerup()




class Booster(Player):
    def __init__(self, color, start_pos, velocity):
        self.power = "BOOST"
        self.powerups_remaining = PLAYERLIVES
        self.speed = velocity

        super().__init__(color, start_pos, velocity)

    def reset(self):
        self.speed = self.init_velocity

        super().reset()

    def setVelocity(self, velocity):
        self.setImage(velocity)
        self.velocity = (sign(velocity[0]) * self.speed, sign(velocity[1]) * self.speed)
        self.newTrail()

    def powerup(self):
        if self.powerup_active == False:
            self.powerup_active = True
            self.powerup_time = POWERUPTIME * FPS

            self.speed = int(self.init_velocity * SPEEDBOOSTFACTOR)
            self.setVelocity(self.velocity)

    def check_powerup(self):
        if (self.powerup_time > 0):
            self.powerup_time -= 1
        else:
            self.powerup_active = False
            self.speed = self.init_velocity

            self.setVelocity(self.velocity)

class Invisible(Player):
    def __init__(self, color, start_pos, velocity):
        self.power = "INVISIBLE"
        self.powerups_remaining = PLAYERLIVES

        super().__init__(color, start_pos, velocity)

    def powerup(self):
        if self.powerup_active == False:
            self.powerup_active = True
            self.powerup_time = POWERUPTIME * FPS
            self.invulnerable = True

            # Invisiblity Bike Color
            self.setDesign(self.velocity, "BLUE")

            # End Trail
            self.activeTrail.endTrail()
            self.lastActiveTrail = self.activeTrail
            self.activeTrail = None

    def check_powerup(self):
        if (self.powerup_time > 0):
            self.powerup_time -= 1
        else:
            self.powerup_active = False
            self.invulnerable = False

            self.newTrail()
            self.setDesign(self.velocity, self.color)


    def setImage(self, new_vel):
        super().setImage(new_vel)

        if self.powerup_active:
            self.setDesign(new_vel, "BLUE")

    def setVelocity(self, velocity):
        """ Change the speed of the player"""
        self.setImage(velocity)
        self.velocity = velocity

        if not self.powerup_active:
            self.newTrail()

    def setDesign(self, vel, color):
            if (vel[0] != 0):
                if (vel[0] < 0):
                    self.image = pygame.image.load(getImages(color)[3])
                else:
                    self.image = pygame.image.load(getImages(color)[1])
            else:
                if (vel[1] < 0):
                    self.image = pygame.image.load(getImages(color)[0])
                else:
                    self.image = pygame.image.load(getImages(color)[2])

            self.image.set_colorkey(WHITE)





