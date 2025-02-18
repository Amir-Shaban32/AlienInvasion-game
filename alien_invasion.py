import sys
import pygame
from random import randint
import time
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from alienbullet import AlienBullet
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard
from game_over_button import GameOverButton


class Aliens:
    """manage behaviour of game"""

    def __init__(self):

        pygame.init()
        self.stop_game = True
        self.game_over = False

        self.setting = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.setting.screen_width = self.screen.get_rect().width
        self.setting.screen_height = self.screen.get_rect().height

        self.ship = Ship(self)
        # manage multiple objects
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.alien_bullets = pygame.sprite.Group()

        self.stats = GameStats(self)
        # instances to show on screen
        self.play_button = Button(self, "Fire!")
        self.game_over_button = GameOverButton(self, "Game Over!")
        self.exit = [pygame.K_q, pygame.K_ESCAPE]

        self.score_board = ScoreBoard(self)

        pygame.display.set_caption("Aliens Invasion")

        self.clock = pygame.time.Clock()

    def run_game(self):
        """Start the game"""
        while True:
            self._check_events()

            if not self.stop_game:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._create_fleet_alien_bullets()
                self._update_alien_bullets()

            self._update_screen()
            self.clock.tick(
                self.setting.game_rate
            )  # framrate loop run 60times per second

    def _check_events(self):
        """Check User Inputs events"""
        for event in pygame.event.get():  # dealing with user inputs/actions
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_play_button()

    def _check_play_button(self):
        """Check if player clicks on screen to start and restart the game"""
        if self.game_over:
            self.game_over = False
        self.stats.reset_stats()
        self.score_board.prep_score()
        self.score_board.prep_ships()
        self.stop_game = False
        self.bullets.empty()
        self.aliens.empty()
        self.alien_bullets.empty()
        self._create_fleet()
        self.ship._recenter_ship()
        self.setting._dynamic_settings()
        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Start Game then,Check Key press"""
        if event.key in self.ship.right_k:
            self.ship.moving_right = True
        elif event.key in self.ship.left_k:
            self.ship.moving_left = True
        elif event.key in self.ship.up_k:
            self.ship.moving_up = True
        elif event.key in self.ship.down_k:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullets()
        elif event.key in self.exit:
            sys.exit()

    def _check_keyup_events(self, event):
        """Check Key release"""
        if event.key in self.ship.right_k:
            self.ship.moving_right = False
        if event.key in self.ship.left_k:
            self.ship.moving_left = False
        if event.key in self.ship.up_k:
            self.ship.moving_up = False
        if event.key in self.ship.down_k:
            self.ship.moving_down = False

    def _fire_bullets(self):
        """Create and fire a bullet."""
        if len(self.bullets) < self.setting.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update bullets and remove old"""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_aliens_collisions()

    def _check_bullet_aliens_collisions(self):
        """Check Collision between bullets and aliens and if there is no aliens create new!"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        # increase score for each alien
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.setting.alien_score * len(aliens)
            self.score_board.prep_score()
            self.score_board.check_high_score()
            self.score_board.prep_level()

        if not self.aliens:
            self.bullets.empty()
            self.alien_bullets.empty()
            self._create_fleet()
            self.setting._increase_speed()

            # increae level
            self.stats.level += 1
            self.score_board.prep_level()

    def _create_fleet(self):
        """Create fleet of aliens"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        while current_y < self.setting.screen_height - 8 * alien_width:
            while current_x < self.setting.screen_width - 2 * alien_width:
                offset_x = randint(-5, 5)
                offset_y = randint(-5, 5)
                self._create_alien(current_x + offset_x, current_y + offset_y)
                current_x += 2 * alien_width  # to separate between two aliens
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """create aliens"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Check one alien reaches edge or not"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._chage_fleet_direction()
                break

    def _chage_fleet_direction(self):
        """Take step down then chage fleet direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.setting.fleet_drop_speed
        self.setting.fleet_direction *= -1

    def _update_aliens(self):
        """Check if fleet reach edge,then update positions"""
        self._check_fleet_edges()
        self.aliens.update()
        # if collision call ship hit
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_alien_buttom()

    def _create_fleet_alien_bullets(self):
        """Create fleet of alien bullets"""
        alien = Alien(self)
        alien_width = alien.rect.width
        current_x = alien_width
        offset_x = randint(-10, 1000)
        while current_x < self.setting.screen_width - offset_x * alien_width:
            self._fire_alien_bullets(current_x)
            current_x += 4 * alien_width

    def _fire_alien_bullets(self, x_position):
        """Make aliens fire ship"""
        if len(self.alien_bullets) < self.setting.alien_bullet_allowed:
            new_alien_bullet = AlienBullet(self)
            new_alien_bullet.x = x_position
            new_alien_bullet.rect.x = x_position
            self.alien_bullets.add(new_alien_bullet)

    def _update_alien_bullets(self):
        """update bullets positions and remove old"""
        self.alien_bullets.update()
        for alien_bullet in self.alien_bullets.copy():
            if alien_bullet.rect.top >= self.screen.get_rect().bottom:
                self.alien_bullets.remove(alien_bullet)
        self._check_alienbullet_ship_collision()

    def _check_alienbullet_ship_collision(self):
        """Check if aliens bullets collided with the ship"""
        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
            self._ship_hit()

    def _check_alien_buttom(self):
        """Check aliens reach bottom of screen or not"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen.get_rect().bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        """Decrease number of ships and restart the game"""
        if self.stats.ship_left > 0:
            self.stats.ship_left -= 1
            self.score_board.prep_ships()
            self.score_board.prep_level()
            self.stats.reset_stats()
            # reset bullets , aliens and alien bullets
            self.bullets.empty()
            self.aliens.empty()
            self.alien_bullets.empty()
            # recenter ship in screen button,then create aliens fleet
            self.score_board.prep_score()
            self._create_fleet()
            self.ship._recenter_ship()
            # stop some little time
            time.sleep(0.2)
        else:
            self.stop_game = True
            self.game_over = True

    def _update_screen(self):
        """Update images on screen , and flip to new screen"""
        self.screen.fill(self.setting.bg_color)
        for star in self.setting.stars:
            pygame.draw.circle(self.screen, self.setting.star_colors, star, 2)
        # draw score right upper screen
        self.score_board._draw_score()
        # draw bullet up screen
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # draw ship
        self.ship.blitme()
        # draw alien bullet
        for alien_bullet in self.alien_bullets:
            alien_bullet.draw_alien_bullet()
        self.aliens.draw(self.screen)
        # show fire button
        if self.stop_game:
            self.play_button._draw_button()
        # show game over button
        if self.game_over:
            self.game_over_button._draw_button()

        pygame.display.flip()


if __name__ == "__main__":

    alienInv = Aliens()
    alienInv.run_game()
