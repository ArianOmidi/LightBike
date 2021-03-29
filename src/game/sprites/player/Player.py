from utils.Util import *
from ..trail.Trail import Trail

import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, color, start_pos, velocity):
        # Call parent class constructor
        super().__init__()

        # Variables
        self.color = color
        self.lives = PLAYER_LIVES

        # Powerup Variables
        self.power = "None"
        self.powerup_active = False
        self.invulnerable = False
        self.powerup_time = 0
        self.color_change_time = 0

        # Set Velocity and Position
        self.init_velocity = velocity
        self.init_pos = start_pos
        self.velocity = (velocity, 0)

        # Sets Image (orientation and color of the bike)
        self.setImage(self.velocity, self.color)

        self.rect = self.image.get_rect()
        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]

        # Sets Trail
        self.activeTrail = None
        self.newTrail()




    # --- Setters --- #

    # Sets design and changes rectangle pos if bike is moving in a different dir
    def setImage(self, new_vel, color):
        self.cur_design = color
        self.image = getBike(new_vel, color)

        if getUnitVector(self.velocity) != getUnitVector(new_vel):
            change_x = change_y = 0
            old_pos = (self.rect.x, self.rect.y)

            if (new_vel[0] != 0):
                if (new_vel[0] < 0):
                    change_x -= PLAYER_WIDTH

                if (self.velocity[1] > 0):
                    change_y += PLAYER_WIDTH
            else:
                if (new_vel[1] < 0):
                    change_y -= PLAYER_WIDTH

                if (self.velocity[0] > 0):
                    change_x += PLAYER_WIDTH

            self.rect = self.image.get_rect()
            self.rect.x = old_pos[0] + change_x
            self.rect.y = old_pos[1] + change_y

    # Set new velocity
    def setVelocity(self, velocity):
        """ Change the speed of the player"""
        self.setImage(velocity, self.cur_design)
        self.velocity = velocity
        self.newTrail()

    # Set new trail
    def newTrail(self):
        if self.activeTrail != None:
            self.activeTrail.endTrail()
        self.lastActiveTrail = self.activeTrail
        self.activeTrail = Trail(self, getTrailColor(self.color, self.powerup_active), (self.rect.x, self.rect.y))

    # --- Powerup Classes --- #

    # def powerup(self):

    # def check_powerup(self):

    def powerup_time_warning(self):
        # Change Bike color to inform player that the powerup is running out
        # Color changes faster when there is less time
        if (self.powerup_time < BOOSTER_POWERUP_TIME * FPS / 1.75):
            if self.color_change_time == 0:
                self.color_change_time = self.powerup_time // (BOOSTER_POWERUP_TIME * 2)

                if (self.color_change_time < FPS // 10):
                    self.color_change_time = FPS // 10

                if self.cur_design == self.color:
                    self.setImage(self.velocity, "POWERUP_" + self.color)
                else:
                    self.setImage(self.velocity, self.color)

            self.color_change_time -= 1


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
        self.velocity = (self.init_velocity, 0)
        self.powerups_remaining = getNumOfPowerups(self.power)
        self.cur_design = self.color

        self.image = getBike(self.velocity, self.color)

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






