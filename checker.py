class Checker():
	def __init__(self, checker_sprite):
		self.checker_sprite = checker_sprite
	

	def draw(self, surface, position):
		pos_x = (position[0] - 63 / 2) - 25
		#pos_x += (pos_x / 2) - 25
		pos_y = (position[1] - 63 / 2) - 25 
		surface.blit(self.checker_sprite, (pos_x, pos_y))