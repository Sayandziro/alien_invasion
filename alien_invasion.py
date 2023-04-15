import sys
import pygame
from settings import Settings
from ship import Ship
from alien import Alien
from bullet import Bullet


class AlienInvasion:
	""" Overall class to manage game assets and behavior. """

	def __init__(self):
		"""Initialize the game, and create game resources."""
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height), pygame.FULLSCREEN)
		pygame.display.set_caption("Alien Invasion")
   		
		self.ship = Ship(self)

		self.bullets = pygame.sprite.Group()

		self.aliens = pygame.sprite.Group()

		self.alien_resources = pygame.image.load("images\\alien.png")

		self._create_fleet()


	def run_game(self):
		"""Start the main loop for the game."""

		while True:
			self._check_events()
			self.ship.update()
			self.bullets.update()
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


	def _create_fleet(self):
		""" Create the fleet of aliens. """

		# Make an alien and find the number of aliens in a row.
		# Spacing between each alien is equal to one alien width.
		alien = Alien(self, self.alien_resources)
		alien_width = alien.rect.width
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width)


		# Create the first row of aliens.
		for alien_number in range(number_aliens_x):
			self._create_alien(alien_number)


	def _create_alien(self, alien_number):
		alien = Alien(self, self.alien_resources)
		alien_width = alien.rect.width
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		self.aliens.add(alien)


	def _update_screen(self):
		"""Update images on the screen, and flip to the new screen."""
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()

		# Draw the bullet if it is not out of the screen, else delete it from sprites.
		for bullet in self.bullets.sprites():
			if bullet.rect.bottom > 0: 
				bullet.draw_bullet()
			else:
				self.bullets.remove(bullet)

		self.aliens.draw(self.screen)

		pygame.display.flip()



if __name__ == "__main__":
	# Make a game instance, and run the game.
	ai = AlienInvasion()
	ai.run_game()