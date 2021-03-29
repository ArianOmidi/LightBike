from utils.Util import *
from .Trail import Trail

import pygame 

class Wall(Trail):
    def __init__(self, player, color, start_pos, old_trail):
        super().__init__(player, color, start_pos)

        wall_pos = (self.rect.x, self.rect.y)

        self.image = pygame.Surface((self.image.get_width() + hasValue(self.dir[0]) * (old_trail.image.get_width()),
                                     self.image.get_height() + hasValue(self.dir[1]) * (old_trail.image.get_height())))
        self.add_design()

        self.rect = self.image.get_rect()

        if (old_trail.dir[0] > 0 or old_trail.dir[1] > 0):
            self.rect.x = old_trail.rect.x
            self.rect.y = old_trail.rect.y
        else:
            self.rect.x = wall_pos[0]
            self.rect.y = wall_pos[1]

        self.dir = (self.dir[0] * WALL_SPEED_FACTOR, self.dir[1] * WALL_SPEED_FACTOR)

    # Return false if out of bounds
    def update(self):
        if not (self.rect.x + self.dir[0] < BORDER_WIDTH or self.rect.y + self.dir[
            1] < BORDER_TOP_OFFSET + BORDER_WIDTH or self.image.get_height() + self.rect.y + self.dir[
                    1] > SCREEN_HEIGHT - BORDER_WIDTH or self.image.get_width() + self.rect.x + self.dir[
                    0] > SCREEN_WIDTH - BORDER_WIDTH):
            super().update()

            return True

        return False

    def endTrail(self):
        return None
