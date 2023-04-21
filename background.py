import pygame


class Background(pygame.sprite.Sprite):
	def __init__(self, image, location):
		pygame.sprite.Sprite.__init__(self)    # Call Sprite initializer.
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location