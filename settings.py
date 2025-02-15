import random


class Settings:

    def __init__(self):
        self.screen_width = 2500
        self.screen_height = 800
        self.bg_color = (10, 10, 50, 80)
        self.star_colors = (255, 255, 255)
        self.stars = [
            (
                random.randint(0, self.screen_width),
                random.randint(0, self.screen_height),
            )
            for _ in range(300)
        ]
        self.game_rate = 60

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 10

        # alien setting
        self.fleet_drop_speed = 10

        # alien bullet settings
        self.alien_bullet_color = (0, 255, 0)
        self.alien_bullet_width = 3
        self.alien_bullet_height = 15
        self.alien_bullet_allowed = 30
        # ship_hit
        self.ships_allowed = 3
        # increase speed settings for each level
        self.speed_up_scale = 1.5
        # score for killing each alien
        self.alien_score = 10

        self._dynamic_settings()

    def _dynamic_settings(self):
        """Initialize dynamic settings"""
        self.alien_bullet_speed = 2
        self.bullet_speed = 10
        self.ship_speed = 3
        self.alien_speed = 1.3
        # 1 for right -1 for left
        self.fleet_direction = 1

    def _increase_speed(self):
        """Increae increasable settings when level up"""
        self.ship_speed *= self.speed_up_scale
        self.bullet_speed *= self.speed_up_scale
        self.alien_speed *= self.speed_up_scale
        self.alien_bullet_speed *= self.speed_up_scale
        self.alien_score = int(self.alien_score * self.speed_up_scale)
