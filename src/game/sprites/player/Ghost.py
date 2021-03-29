from utils.Util import *
from .Player import Player
from ..trail.Trail import Trail

import pygame

class Ghost(Player):
    def __init__(self, color, start_pos, velocity):
        super().__init__(color, start_pos, velocity)

        self.power = "GHOST"
        self.powerups_remaining = getNumOfPowerups(self.power)


    # --- Setters --- #

    def setVelocity(self, velocity):
        # Set image and color if powerup is active
        self.setImage(velocity, self.cur_design)
        self.velocity = velocity

        if not self.powerup_active:
            self.newTrail()

    # --- Powerup Functions --- #

    def powerup(self):
        if self.powerup_active == False and self.powerups_remaining > 0:
            self.powerups_remaining -= 1
            self.powerup_active = True
            self.powerup_time = INVISIBLE_POWERUP_TIME * FPS
            self.invulnerable = True

            # Invisiblity Bike Color
            self.setImage(self.velocity, "POWERUP_" + self.color)

            # End Trail
            self.activeTrail.endTrail()
            self.lastActiveTrail = self.activeTrail
            self.activeTrail = None

            # Play Sound
            SOUND_PLAYER.play_ghost()

    def check_powerup(self):
        if (self.powerup_time > 0):
            self.powerup_time_warning()
            self.powerup_time -= 1
        else:   # If powerup time is over turn off invisibility and set regular design
            self.powerup_active = False
            self.invulnerable = False

            self.newTrail()
            self.setImage(self.velocity, self.color)