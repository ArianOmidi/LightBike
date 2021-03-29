from utils.Util import *
from .Trail import Trail

import pygame 

class BoostTrail(Trail):
    def __init__(self, player, color, start_pos):
        super().__init__(player, color, start_pos)

    def add_design(self):
        super().add_design()

        num_of_dots = ceil((self.image.get_width() * hasValue(self.dir[0]) + self.image.get_height() * hasValue(
            self.dir[1])) // BOOST_TRAIL_DIVIDER)

        for i in range(0, num_of_dots):
            dot = pygame.Surface((self.size, self.size))
            dot.fill(BACKGROUND)

            if (self.dir[0] > 0 or self.dir[1] > 0):
                self.image.blit(dot, (
                    BOOST_TRAIL_DIVIDER * self.size * i * hasValue(self.dir[0]),
                    BOOST_TRAIL_DIVIDER * self.size * i * hasValue(self.dir[1])))
            else:
                self.image.blit(dot, (
                    (self.image.get_width() - BOOST_TRAIL_DIVIDER * self.size * (i + 1)) * hasValue(self.dir[0]),
                    (self.image.get_height() - BOOST_TRAIL_DIVIDER * self.size * (i + 1)) * hasValue(self.dir[1])))

