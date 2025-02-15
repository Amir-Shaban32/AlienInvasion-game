import pygame


class GameStats:
    """Track state of the game"""

    def __init__(self, alienInv):
        """Initialize and Track stats of the game!!"""
        self.setting = alienInv.setting
        # details on screen
        self.high_score = 0
        self.level = 1

        self.reset_stats()

    def reset_stats(self):
        """Manage number of ships"""
        self.ship_left = self.setting.ships_allowed
        self.score = 0
