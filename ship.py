import pygame


class Ship:
	"""A class to manage the ship."""

	def __init__(self, ai_game):
		"""Initialize the ship and set its starting position."""
		self.screen = ai_game.screen
		self.screen_rect = ai_game.screen.get_rect()
		self.settings = ai_game.settings

		# Load the ship image, get and change its dimensions and get its rect.
		self.image = pygame.image.load("images\\ship.bmp")
		self.width = self.image.get_rect().width
		self.height = self.image.get_rect().height
		self.image = pygame.transform.smoothscale(self.image, (self.width/4, self.height/4))
		self.rect = self.image.get_rect()

		# Start each new ship at the bottom center of the screen.
		self.rect.x = 885
		self.rect.y = 850
		self.x_y = [self.rect.x, self.rect.y]

		# Movement flags.
		self.moving_right = False
		self.moving_left = False

		# Store a decimal value for the ships horizontal position
		self.x = float(self.rect.x)


	def update(self):
		"""Update the ship's position based on the movement flag."""

		# Update the ship's x value, not the rect.
		if self.moving_right:
			self.x += self.settings.ship_speed
		if self.moving_left:
			self.x -= self.settings.ship_speed

		# Update rect object form self.x
		self.x_y[0] = self.x


	def blitme(self):
		"""Draw the ship at its current location."""
		self.screen.blit(self.image, self.x_y)
		