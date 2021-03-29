from utils.Util import *
from .Player import Player
from ..trail.Trail import Trail

import pygame

class Jumper(Player):
    def __init__(self, color, start_pos, velocity):
        super().__init__(color, start_pos, velocity)

        self.power = "JUMPER"
        self.powerups_remaining = getNumOfPowerups(self.power)
        self.in_jump = False


    # --- Powerup Functions --- #

    def powerup(self):
        if self.powerup_active == False and self.powerups_remaining > 0:
            self.powerups_remaining -= 1
            self.powerup_active = True
            self.powerup_time = JUMPER_POWERUP_TIME * FPS

        self.jump()

    def check_powerup(self):
        if (self.powerup_time > 0):
            self.powerup_time_warning()
            self.powerup_time -= 1
        else:  # If powerup time is over turn off invisibility and set regular design
            self.powerup_active = False
            self.setImage(self.velocity, self.color)

    def jump(self):
        if not self.in_jump:
            self.in_jump = True
            self.invulnerable = True
            self.jump_time_remaining = JUMP_TIME * FPS

            # End Trail
            self.activeTrail.endTrail()
            self.lastActiveTrail = self.activeTrail
            self.activeTrail = None

            SOUND_PLAYER.play_jump()

    def check_jump(self):
        if (self.jump_time_remaining > 0):
            self.jump_time_remaining -= 1
        else:
            self.in_jump = False
            self.invulnerable = False
            self.newTrail()


    # --- Setters --- #

    def setVelocity(self, velocity):
        # Cant change velocity mid-jump
        if not self.in_jump:
            super().setVelocity(velocity)

    def update(self):
        super().update()

        if self.in_jump:
            self.check_jump()

