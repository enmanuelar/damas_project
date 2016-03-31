import pygame 

class Board():
	def __init__(self, x, y, board_sprite, checker_sprite, board_array):
		self.x = x
		self.y = y
		self.board_sprite = board_sprite
		self.checker_sprite = checker_sprite
		self.board_width = self.board_sprite.get_width()
		self.board_height = self.board_sprite.get_height()
		self.checker_width = self.checker_sprite.get_width()
		self.checker_height = self.checker_sprite.get_height()
		self.board_array = board_array


	def draw(self, surface):
		surface.blit(self.board_sprite,(self.x, self.y))

	def initialize(self, initial_row, player_num, player_pos):
		pos_x = ((self.board_width / 8) / 2) - (self.checker_width / 2)

		if player_pos == "top":
			pos_y = ((self.board_height / 8) / 2) - (self.checker_height / 2)
		else:
			pos_y = ((self.board_height / 2) + (self.board_height / 8)) + (self.checker_height / 8)

		for y in range(initial_row, len(self.board_array)):
			i = 0
			for x in self.board_array[y]:
				if x == 1 and y < (initial_row + 3):
					self.board_array[y][i] = player_num
					return [pos_x, pos_y]
				else:
					pos_x += (self.board_width / 8)
					i += 1
			pos_x = ((self.board_width / 8) / 2) - (self.checker_width / 2)
			pos_y += (self.board_height / 8)			


	def get_board_width(self):
		return self.board_width

	def get_board_height(self):
		return  self.board_height