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
		self.image = pygame.transform.smoothscale(self.image, (self.width/5, self.height/5))
		self.rect = self.image.get_rect()

		# Start each new ship at the bottom center of the screen.
		# self.rect.x = 885.0
		# self.rect.y = 850.0
		self.rect.midbottom = self.screen_rect.midbottom

		self.x = float(self.rect.x)

		# Movement flags.
		self.moving_right = False
		self.moving_left = False


	def update(self):
		"""Update the ship's position based on the movement flag."""

		# Update the ship's rect.x value.
		if self.moving_right and self.rect.x < self.settings.screen_width:
			self.x += self.settings.ship_speed
		if self.moving_left and self.rect.x >= 0:
			self.x -= self.settings.ship_speed

		self.rect.x = self.x


	def blitme(self):
		"""Draw the ship at its current location."""
		self.screen.blit(self.image, self.rect)
		