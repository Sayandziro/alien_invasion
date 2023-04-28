class Settings:
	"""A class to store all settings for Alien Invasion."""

	def __init__(self):
		"""Initialize the game's settings."""
		# Screen settings
		self.screen_width = 1450
		self.screen_height = 800
		self.bg_color = (255, 255, 255)

		# Ship settings
		self.ship_limit = 2

		# Bullet settings
		self.bullet_width = 4
		self.bullet_height = 25
		self.bullet_color = (220, 20, 60)
		self.bullets_allowed = 5

		# Alien settings
		self.alien_speed = 3.0
		self.fleet_drop_speed = 100

		# How quickly the game speeds up
		self.speedup__scale = 1.1

		# How quickly the alien point values increase.
		self.score_scale = 1.5

		self.initialize_dynamic_settings()


	def initialize_dynamic_settings(self):
		""" Inintialize settings that change throughout the game. """
		self.ship_speed = 7.0
		self.bullet_speed = 5.0
		self.alien_speed = 2.5

		# fleet_direction of 1 represents right; -1 represents left.
		self.fleet_direction = 1

		# Scoring
		self.alien_points = 50


	def increase_speed(self):
		""" Increase speed settings and alien point values. """
		self.ship_speed *= self.speedup__scale
		self.bullet_speed *= self.speedup__scale
		self.alien_speed *= self.speedup__scale

		self.alien_points = int(self.alien_points * self.score_scale)