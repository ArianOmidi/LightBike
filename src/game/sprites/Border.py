from utils.Util import *

import pygame

class Border(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()

        self.image = pygame.Surface(size)
        self.add_design()

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def add_design(self):
        self.image.fill(BORDERCOLOR)

        # Stripe
        stripe = pygame.Surface(
            (self.image.get_width() - (2 * (BORDER_WIDTH // 2)), self.image.get_height() - (2 * (BORDER_WIDTH // 2))))
        stripe.fill(BACKGROUND)
        self.image.blit(stripe, (BORDER_WIDTH // 2, BORDER_WIDTH // 2))