import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, alienInv):
        """Draw image and control it's behaviour"""
        super().__init__()
        self.screen = alienInv.screen
        self.screen_rect = alienInv.screen.get_rect()  # make screen as rectangle
        self.setting = alienInv.setting

        self.image = pygame.image.load("images/spaceship.bmp")
        new_size = (100, 100)
        self.image = pygame.transform.scale(self.image, new_size)
        self.rect = self.image.get_rect()  # make ship as rectangle

        self.rect.midbottom = (
            self.screen_rect.midbottom
        )  # initialize ship at middbottom

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.right_k = [pygame.K_RIGHT, pygame.K_d]
        self.left_k = [pygame.K_LEFT, pygame.K_a]
        self.up_k = [pygame.K_UP, pygame.K_w]
        self.down_k = [pygame.K_DOWN, pygame.K_s]

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update Ship position based on keypress"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.setting.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.setting.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.setting.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.setting.ship_speed

        self.rect.x = self.x
        self.rect.y = self.y

    def _recenter_ship(self):
        """Restart original position of the Ship"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        self.screen.blit(self.image, self.rect)  # draw image
