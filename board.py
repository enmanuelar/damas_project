import pygame 

class Board():
	def __init__(self, x, y, board_sprite, board_array):
		self.x = x
		self.y = y
		self.board_sprite = board_sprite
		self.board_width = self.board_sprite.get_width()
		self.board_height = self.board_sprite.get_height()
		self.board_array = board_array


	def draw(self, surface):
		surface.blit(self.board_sprite,(self.x, self.y))
		

	def initialize(self, initial_row, player_num):
		for y in range(initial_row, len(self.board_array)):
			i = 0
			for x in self.board_array[y]:
				if x == 1 and y < (initial_row + 3):
					self.board_array[y][i] = player_num
				i += 1

	def get_coordinates(self):
		coord_x, coord_y = 0, 0
		coordinates = []
		row_coord = []
		for y in range(8):
			coord_y += self.board_height / 8
			for x in range(8):
				coord_x += self.board_width / 8
				row_coord.append([coord_x, coord_y])
			coordinates.append(row_coord)
			row_coord = []
			coord_x = 0
		return coordinates

	def get_board_width(self):
		return self.board_width

	def get_board_height(self):
		return  self.board_height

	def get_checker_index(self, coordinates_array, mouse_pos):
		for row in coordinates_array:
			for space in row:
				if mouse_pos[0] < space[0] and mouse_pos[1] < space[1]:
					row_index = coordinates_array.index(row)
					space_index = row.index(space)
					return row_index, space_index

	def get_space_value(self, row_index, space_index):
		return self.board_array[row_index][space_index]

	def get_space_coordinates(self, coordinates_array, row_index, space_index):
		return coordinates_array[row_index][space_index]

	def get_next_row_coordinates(self, coordinates_array, current_checker, row_index, space_index):
		if current_checker == 3:
			try:
				if space_index == 0:
					return [[coordinates_array[row_index - 1][space_index + 1]]]
				else:
					next_pos = [[coordinates_array[row_index - 1][space_index - 1]], [coordinates_array[row_index - 1][space_index + 1]]]
 					return next_pos
 			except IndexError:
 				next_pos = [[coordinates_array[row_index - 1][space_index - 1]]]
 				return next_pos
 		else:
 			if current_checker == 2:
 				try:
					if space_index == 0:
						return [[coordinates_array[row_index + 1][space_index + 1]]]
					else:
						next_pos = [[coordinates_array[row_index + 1][space_index - 1]], [coordinates_array[row_index + 1][space_index + 1]]]
	 					return next_pos
	 			except IndexError:
	 				next_pos = [[coordinates_array[row_index + 1][space_index - 1]]]
	 				return next_pos

	#devuelve true si los dos espacios siguientes son 1 o false si encuentra una ficha
	def check_next_row(self):
		pass


	def move_checker(self, coordinates_array, mouse_pos, release_space_value, current_checker, checker_list_index, first_row_index, first_space_index):
		row_index, space_index = self.get_checker_index(coordinates_array, mouse_pos)
		#current_checker = self.get_space_value(row_index, space_index)
		if release_space_value == 1:
			if( 

				current_checker == 3			
				):
				self.board_array[first_row_index][first_space_index] = 1
				self.board_array[row_index][space_index] = 3
			else:
				if( 
					(mouse_pos[0] < coordinates_array[first_row_index + 1][first_space_index - 1] or
					mouse_pos[0] < coordinates_array[first_row_index + 1][first_space_index + 1]) and
					current_checker == 2			
					):
					self.board_array[first_row_index][first_space_index] = 1
					self.board_array[row_index][space_index] = 2

	def init_turn(self, first_player):
		turn = {"top": [2, 4], "bottom": [3, 5]}
		return turn[first_player]

	def change_turn(self, current_turn):
		turn = {"top": [2, 4], "bottom": [3, 5]}
		if current_turn == turn["bottom"]:
			current_turn = turn["top"]
		else:
			if current_turn == turn["top"]:
				current_turn = turn["bottom"]
		return current_turn


