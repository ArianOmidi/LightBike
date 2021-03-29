from utils.Util import *
from .Player import Player
from ..trail.Trail import Trail
from ..trail.Wall import Wall

import pygame

class Builder(Player):
    def __init__(self, color, start_pos, velocity):
        super().__init__(color, start_pos, velocity)

        self.power = "BUILDER"
        self.powerups_remaining = getNumOfPowerups(self.power)

        self.new_wall_made = False
        self.deleted_trail = None


    # --- Powerup Functions --- #

    def powerup(self):
        if self.powerup_active == False and self.powerups_remaining > 0:
            self.powerups_remaining -= 1
            self.powerup_active = True
            self.powerup_time = BUILDER_POWERUP_TIME * FPS

            self.newWall()

            # Play Sound
            SOUND_PLAYER.play_wall()

    def check_powerup(self):
        if (self.powerup_time > 0 and self.wall.update()):
            self.powerup_time -= 1
        else:  # If powerup time is over turn off invisibility and set regular design
            self.powerup_active = False


    def newWall(self):
        self.new_wall_made = True
        self.deleted_trail = self.activeTrail

        self.wall = Wall(self, getTrailColor(self.color, self.powerup_active), (self.rect.x, self.rect.y),
                         self.deleted_trail)
        self.activeTrail = self.wall

    # --- Setters --- #

    def newTrail(self):
        self.new_wall_made = False

        if self.activeTrail != None and not isinstance(self.activeTrail, Wall):
            self.activeTrail.endTrail()
        self.lastActiveTrail = self.activeTrail
        self.activeTrail = Trail(self, getTrailColor(self.color, self.powerup_active), (self.rect.x, self.rect.y))

    def update(self):
        """ Find a new position for the player"""
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if (self.activeTrail is not None) and (not isinstance(self.activeTrail, Wall)):
            self.activeTrail.update()

        if self.powerup_active:
            self.check_powerup()
