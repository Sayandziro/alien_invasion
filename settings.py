class Settings:
	"""A class to store all settings for Alien Invasion."""

	def __init__(self):
		"""Initialize the game's settings."""
		# Screen settings
		self.screen_width = 1450
		self.screen_height = 800
		self.bg_color = (255, 255, 255)

		# Ship settings
		self.ship_speed = 7
		self.ship_limit = 3

		# Bullet settings
		self.bullet_speed = 5
		self.bullet_width = 400
		self.bullet_height = 25
		self.bullet_color = (220, 20, 60)
		self.bullets_allowed = 5

		# Alien settings
		self.alien_speed = 3.0
		self.fleet_drop_speed = 20
		# fleet_direction of 1 represents right; -1 represents left.
		self.fleet_direction = 1
