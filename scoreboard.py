import pygame.font
from pygame.sprite import Group
from ship import Ship


class ScoreBoard:
    """A class to report scoring information."""

    def __init__(self, alienInv):
        """Initialize scorekeeping attributes."""
        self.ai_game = alienInv
        self.screen = alienInv.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = alienInv.setting
        self.stats = alienInv.stats

        # Font settings for scoring information.
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color
        )

        # Display the score at the top right of the screen.
        self.score_image_rect = self.score_image.get_rect()
        self.score_image_rect.right = self.screen_rect.right - 30
        self.score_image_rect.top = 20

    def prep_high_score(self):
        """Prepare high score image"""
        rounde_high_score = round(self.stats.high_score, -1)
        high_score_str = f"Max:{rounde_high_score:,}"
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.settings.bg_color
        )

        self.high_score_image_rect = self.high_score_image.get_rect()
        self.high_score_image_rect.topleft = self.screen_rect.topleft

    def prep_level(self):
        """prepare level image"""
        level_str = str(self.stats.level)
        self.level_message = self.font.render(
            level_str, True, self.text_color, self.settings.bg_color
        )
        self.level_message_rect = self.level_message.get_rect()
        self.level_message_rect.right = self.score_image_rect.right
        self.level_message_rect.top = self.score_image_rect.bottom + 10

    def prep_ships(self):
        """prepare ships lefted on image"""
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_game)
            ship.rect.x = self.screen_rect.right - 100 - ship_number * ship.rect.width
            ship.rect.y = self.screen_rect.bottom - 100
            self.ships.add(ship)

    def check_high_score(self):
        """Update max score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def _draw_score(self):
        """Draw score,level,max and remain ships to the screen."""
        self.screen.blit(self.score_image, self.score_image_rect)
        self.screen.blit(self.high_score_image, self.high_score_image_rect)
        self.screen.blit(self.level_message, self.level_message_rect)
        self.ships.draw(self.screen)
