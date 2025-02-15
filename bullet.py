import pygame

from pygame.sprite import Sprite  # manage and update game objects efficiently.


class Bullet(Sprite):
    """Manage bullet fired"""

    def __init__(self, alienInv):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = alienInv.screen
        self.settings = alienInv.setting
        self.color = self.settings.bullet_color

        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height
        )
        self.rect.midtop = alienInv.ship.rect.midtop

        self.y = float(self.rect.y)

    def update(self):
        """Moving bullet to up"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw bullet up ship"""
        pygame.draw.rect(self.screen, self.color, self.rect)
