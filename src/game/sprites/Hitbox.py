from utils.Util import *
from ..sprites.player.Player import Player

import pygame

class Hitbox(pygame.sprite.Sprite):
    def __init__(self, sprite):
        super().__init__()

        self.image = pygame.Surface((sprite.image.get_width(), sprite.image.get_height()))

        if isinstance(sprite, Player):
            self.image.fill(RED)
        else:
            self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = sprite.rect.x
        self.rect.y = sprite.rect.y