class Checker():
	def __init__(self, checker_sprite, checker_sprite_alpha):
		self.checker_sprite = checker_sprite
		self.checker_sprite_alpha = checker_sprite_alpha

	def draw(self, surface, position):
		pos_x = (position[0] - 63 / 2) - 25
		pos_y = (position[1] - 63 / 2) - 25 

		surface.blit(self.checker_sprite, (pos_x, pos_y))

	def draw_on_next_row(self, surface, position):
		pos_x = (position[0] - 63 / 2) - 25
		pos_y = (position[1] - 63 / 2) - 25 
		surface.blit(self.checker_sprite_alpha, (pos_x, pos_y))		
