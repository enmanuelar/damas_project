class Checker():
	def __init__(self, checker_sprite):
		self.checker_sprite = checker_sprite
	

	def draw(self, surface, position):
		surface.blit(self.checker_sprite, (position[0], position[1]))