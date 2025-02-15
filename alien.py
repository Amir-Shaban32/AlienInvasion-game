import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Built a single alien in screen"""

    def __init__(self, alienInv):
        super().__init__()
        self.screen = alienInv.screen
        self.screen_rect = alienInv.screen.get_rect()
        self.setting = alienInv.setting

        self.image = pygame.image.load("images/alien.bmp")
        new_size = (50, 50)
        self.image = pygame.transform.scale(self.image, new_size)
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):
        """Check alien reaches to edge or not"""
        return (self.rect.right >= self.screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """Update position of aliens"""
        self.x += self.setting.alien_speed * self.setting.fleet_direction
        self.rect.x = self.x
