import sys
from time import sleep

from background import Background
import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from alien import Alien
from bullet import Bullet
from button import Button



class AlienInvasion:
	""" Overall class to manage game assets and behavior. """

	def __init__(self):
		"""Initialize the game, and create game resources."""
		pygame.init()

		self.settings = Settings()
		self.bg_image = pygame.image.load("images\\space_background.jpg")
		self.background = Background(self.bg_image, [0, 0])
		self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height), pygame.FULLSCREEN)
		pygame.display.set_caption("Alien Invasion")

		# Create an instance to store game statistics,
		# 	and create a scoreboard.
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)
   		
		self.ship = Ship(self)

		self.bullets = pygame.sprite.Group()

		self.aliens = pygame.sprite.Group()

		self.alien_resources = pygame.image.load("images\\alien.png")

		self._create_fleet()

		# Make the Play button.
		self.play_button = Button(self, "Play")

		self.clock = pygame.time.Clock()


	def run_game(self):
		"""Start the main loop for the game."""

		while True:
			self.clock.tick(120)

			self._check_events()

			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()
			
			self._update_screen()


	def _check_events(self):
		""" Respond to keypresses and mouse events. """
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			elif event.type == pygame.KEYDOWN:
				self._check_keydownn_events(event)

			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)

			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)


	def _check_play_button(self, mouse_pos):
		""" Start a new game when the player clicks Play. """
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			# Reset the game setttings.
			self.settings.initialize_dynamic_settings()
			
			# Reset the game statistics.
			self.stats.reset_stats()
			self.stats.game_active = True

			# Get rid of any remaining aliens and bullets.
			self.aliens.empty()
			self.bullets.empty()

			# Hide the mouse cursor.
			pygame.mouse.set_visible(False)


	def _check_keydownn_events(self, event):
		if event.key == pygame.K_RIGHT:
			# Move the ship to the right.
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			# Move the ship to the left.
			self.ship.moving_left = True 

		elif event.key == pygame.K_SPACE:
			# Fire the bullet on SPACE key.
			self._fire_bullet()

		if event.key == pygame.K_q:
			# Quit the game if q is pressed.
			sys.exit()


	def _check_keyup_events(self, event):
		if event.key == pygame.K_RIGHT:
					self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
					self.ship.moving_left = False


	def _fire_bullet(self):
		""" Create a new bullet and add it to the bullets group. """
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)


	def _update_bullets(self):
		""" Draw the bullet if it is not out of the screen, else delete it from sprites. """
		# Update bullet positions.
		self.bullets.update()

		# Get rid of bullets that have disappeared.
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0: 
				self.bullets.remove(bullet)

		self._check_bullet_alien_collision()

		# Repopulate the fleet if destroyed and destroy the bullets.
		if not self.aliens:
			self.bullets.empty()
			self._create_fleet()


	def _check_bullet_alien_collision(self):
		"""
		 Check for any bullets that have hit aliens.
		   If so, get rid of the bullet and the alien.
		"""
		collisions = pygame.sprite.groupcollide(
				self.bullets, self.aliens, True, True)

		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb.prep_score()
			self.sb.check_high_score()

		# Repopulate the fleet if destroyed and destroy the bullets.
		if not self.aliens:
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()


	def _create_fleet(self):
		""" Create the fleet of aliens. """

		# Make an alien and find the number of aliens in a row.
		# Spacing between each alien is equal to one alien width.
		alien = Alien(self, self.alien_resources)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width) + 1

		# Determine the number of rows of aliens that fit on the screen.
		ship_height = self.ship.rect.height
		available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
		number_of_rows = available_space_y // (2 * alien_height)


		# Create the first row of aliens.
		for row_number in range(number_of_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)


	def _create_alien(self, alien_number, row_number):
		alien = Alien(self, self.alien_resources)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien_height + 2 * alien_height * row_number
		self.aliens.add(alien)


	def _check_fleet_edges(self):
		""" Respond appropriately if any aliens have reached an edge. """
		for alien in self.aliens.sprites():
			if alien.check_edges():
				 self._change_fleet_direction()
				 break


	def _change_fleet_direction(self):
		""" Drop the entire fleet and change the fleet's direction. """
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1


	def _update_aliens(self):
		""" 
		Check if the fleet is at an edge,
			then update the positions of all aliens in the fleet. 
		"""
		self._check_fleet_edges()
		self.aliens.update()

		self._check_alien_ship_collision()

		self._check_aliens_bottom()


	def _check_alien_ship_collision(self):
		""" Look for alien-ship collision and destroy both if so. """
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()


	def _ship_hit(self):
		""" Respond to the ship being hit by an alien. """
		if self.stats.ships_left > 0:
			# Decrement ships left.
			self.stats.ships_left -= 1

			# Get rid of any remaining aliens and bullets.
			self.aliens.empty()
			self.bullets.empty()

			# Create a new fleet and center the ship.
			self._create_fleet()
			self.ship.center_ship()

			# Pause the game.
			sleep(0.5)
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)


	def _check_aliens_bottom(self):
		""" Check if any aliens have reached the bottom of the screen. """
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				# Treat this same as if the ship got hit.
				self._ship_hit()
				break


	def _update_screen(self):
		"""Update images on the screen, and flip to the new screen."""
		self.screen.fill(self.settings.bg_color)
		self.screen.blit(self.background.image, self.background.rect)
			
		if self.stats.game_active:
			self.ship.blitme()
			for bullet in self.bullets.sprites():
				bullet.draw_bullet()
			self.aliens.draw(self.screen)

			# Draw the score information.
			self.sb.show_score()

		# Draw the play button if the game is innactive.
		if not self.stats.game_active:
			self.stats.reset_stats()
			self.sb.prep_score()
			self.play_button.draw_button()

		pygame.display.flip()



if __name__ == "__main__":
	# Make a game instance, and run the game.
	ai = AlienInvasion()
	ai.run_game()