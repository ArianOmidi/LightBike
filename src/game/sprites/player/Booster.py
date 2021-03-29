from utils.Util import *
from .Player import Player
from ..trail.Trail import Trail
from ..trail.BoostTrail import BoostTrail

import pygame

class Booster(Player):
    def __init__(self, color, start_pos, velocity):
        super().__init__(color, start_pos, velocity)

        self.power = "BOOSTER"
        self.powerups_remaining = getNumOfPowerups(self.power)
        self.speed = abs(velocity)

    # --- Setters --- #

    def setVelocity(self, velocity):
        super().setVelocity((sign(velocity[0]) * self.speed, sign(velocity[1]) * self.speed))

    def newTrail(self):
        if self.activeTrail != None:
            self.activeTrail.endTrail()
        self.lastActiveTrail = self.activeTrail

        if self.powerup_active:
            self.activeTrail = BoostTrail(self, getTrailColor(self.color, self.powerup_active),
                                          (self.rect.x, self.rect.y))
        else:
            self.activeTrail = Trail(self, getTrailColor(self.color, self.powerup_active), (self.rect.x, self.rect.y))


    # --- Powerup Functions --- #

    def powerup(self):
        if self.powerup_active == False and self.powerups_remaining > 0:
            self.powerups_remaining -= 1
            self.powerup_active = True
            self.powerup_time = BOOSTER_POWERUP_TIME * FPS

            self.speed = abs(int(self.init_velocity * SPEED_BOOST_FACTOR))
            self.setVelocity(self.velocity)

            SOUND_PLAYER.play_boost()

    def check_powerup(self):
        if (self.powerup_time > 0):
            self.powerup_time_warning()
            self.powerup_time -= 1
        else:
            self.powerup_active = False
            self.speed = abs(self.init_velocity)
            self.cur_design = self.color

            self.setVelocity(self.velocity)

    # --- Other --- #

    def reset(self):
        self.speed = abs(self.init_velocity)

        super().reset()