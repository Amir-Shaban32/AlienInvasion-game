import pygame


class GameOverButton:

    def __init__(self, alienInv, msg):
        """Initialize button properties"""
        self.screen = alienInv.screen
        self.screen_rect = self.screen.get_rect()

        # properties of button
        self.text_color = (0, 0, 0)
        self.button_color = (255, 0, 0)
        self.width, self.height = 50, 50
        self.font = pygame.font.SysFont(None, 100)

        # Create button rect
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn text to image , and center it on button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def _draw_button(self):
        """draw button,then message"""
        self.screen.fill(self.text_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
