

class Checker():
	def __init__(self, sprite_dict, player):
		self.checker_sprite = sprite_dict[player]["sprite"]
		self.sprite_rect = self.checker_sprite.get_rect()
		self.checker_sprite_alpha = sprite_dict[player]["alpha_sprite"]

	def draw(self, surface, position):
		self.sprite_rect.left = (position[0] - 63 / 2) - 25
		self.sprite_rect.top = (position[1] - 63 / 2) - 25
		surface.blit(self.checker_sprite, self.sprite_rect)

	def draw_on_next_row(self, surface, position):
		pos_x = (position[0] - 63 / 2) - 25
		pos_y = (position[1] - 63 / 2) - 25 
		surface.blit(self.checker_sprite_alpha, (pos_x, pos_y))		

