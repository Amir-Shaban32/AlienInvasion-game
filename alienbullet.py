import pygame
from alien import Alien
from pygame.sprite import Sprite


class AlienBullet(Sprite):
    """Create alien bullets to fire ship"""

    def __init__(self, alienInv):
        super().__init__()
        self.screen = alienInv.screen
        self.setting = alienInv.setting
        self.color = self.setting.alien_bullet_color

        self.alien = Alien(alienInv)

        self.rect = pygame.Rect(
            0, 0, self.setting.alien_bullet_width, self.setting.alien_bullet_height
        )

        self.rect.midbottom = self.alien.rect.midbottom

        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update(self):
        """Moving bullet down"""
        self.y += self.setting.alien_bullet_speed
        self.rect.y = self.y

    def draw_alien_bullet(self):
        """Create alien bullets"""
        pygame.draw.rect(self.screen, self.color, self.rect)
