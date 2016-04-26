import pygame 
from pprint import pprint

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
		for y in range(9):
			coord_y += self.board_height / 8
			for x in range(9):
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
		try:
			return self.board_array[row_index][space_index]
		except IndexError:
			pass

	def get_space_coordinates(self, coordinates_array, row_index, space_index):
		return coordinates_array[row_index][space_index]

	def get_coord_index(self, coordinates_array, coordinate_to_check):
		current_row = 0
		index = []
		for row in coordinates_array:
			current_space = 0
			for space in row:
				if space in coordinate_to_check:
					index.append([current_row, current_space])
				current_space += 1
			current_row += 1
		return index

	def get_value_by_coordinates(self, coordinates_array, coordinates_to_check):
		space_values = []		
		row_space_index = self.get_coord_index(coordinates_array, coordinates_to_check)
		space_values.append(self.get_space_value(row_space_index[0][0], row_space_index[0][1]))
		return space_values
	


	def get_next_pos_dict(self, coordinates_array, coordinates_to_check, current_checker):
		next_pos_dict = {}
		next_pos = []
		enemy_pos = []
		while True:
			coord = coordinates_to_check.pop()
			coord_index = self.get_coord_index(coordinates_array, [coord])
			space_value = self.get_space_value(coord_index[0][0], coord_index[0][1])
			if space_value == 1:
				next_pos.append(coord)
			else:
				if current_checker == 4 and (space_value not in (current_checker, 1, 2)):
					enemy_pos.append(coord)
				else:
					if space_value not in (current_checker, 1):
						enemy_pos.append(coord)
			if len(coordinates_to_check) == 0:
				break
		next_pos_dict["next_pos"] = next_pos
		next_pos_dict["enemy_pos"] = enemy_pos
		return next_pos_dict

	def get_next_pos(self, coordinates_array, coordinates_to_check, current_checker, current_coordinate):
		next_pos_dict = self.get_next_pos_dict(coordinates_array, coordinates_to_check, current_checker)
		next_pos = next_pos_dict["next_pos"]
		enemy_pos = next_pos_dict["enemy_pos"]
		index_to_append = 0
		found_new_pos = False
		if len(enemy_pos) > 0:
			for pos in enemy_pos:
				pos_index = self.get_coord_index(coordinates_array, [pos])
				next_space_coord = self.get_next_row_coordinates(coordinates_array, current_checker, pos_index[0][0], pos_index[0][1])
				for next_coord in next_space_coord:
					next_coord_index = self.get_coord_index(coordinates_array, [next_coord])
					space_value = self.get_space_value(next_coord_index[0][0], next_coord_index[0][1])
					if next_coord[0] != current_coordinate[0] and next_coord[1] != current_coordinate[1] and space_value == 1:
						next_pos.append(next_coord)
						found_new_pos = True
				index_to_append += 1
		if found_new_pos:
			for pos in next_pos:
				if ((pos[0] - current_coordinate[0]) * -1) in (63, -63):
					next_pos.remove(pos)
		next_pos_dict["next_pos"] = next_pos
		print next_pos_dict
		return next_pos_dict

	def get_next_row_coordinates(self, coordinates_array, current_checker, row_index, space_index):	
		if current_checker == 2:
			default = [coordinates_array[row_index + 1][space_index - 1], coordinates_array[row_index + 1][space_index + 1]]
			return {0: [coordinates_array[row_index + 1][space_index + 1]],
					7: [coordinates_array[row_index + 1][space_index - 1]]}.get(space_index, default)
		else:
			if current_checker == 3:
				default = [coordinates_array[row_index - 1][space_index - 1], coordinates_array[row_index - 1][space_index + 1]]
				#default = [coordinates_array[row_index + 1][space_index - 1], coordinates_array[row_index + 1][space_index + 1],				
				return {0: [coordinates_array[row_index - 1][space_index + 1]],
						7: [coordinates_array[row_index - 1][space_index - 1]]}.get(space_index, default)
			else:
				if current_checker == 4 or current_checker == 5:
					return self.get_next_row_king(coordinates_array, row_index, space_index)
					
	
	def get_next_row_king(self, coordinates_array, row_index, space_index):
		if row_index == 0:
			default = [coordinates_array[row_index + 1][space_index - 1], coordinates_array[row_index + 1][space_index + 1]]
		else:
			if row_index == 7:
				default = [coordinates_array[row_index - 1][space_index - 1], coordinates_array[row_index - 1][space_index + 1]]
			else:
				default = [coordinates_array[row_index + 1][space_index - 1], coordinates_array[row_index + 1][space_index + 1], coordinates_array[row_index - 1][space_index - 1], coordinates_array[row_index - 1][space_index + 1]]
		return {0: [coordinates_array[row_index - 1][space_index + 1], coordinates_array[row_index + 1][space_index + 1]],
				7: [coordinates_array[row_index - 1][space_index - 1], coordinates_array[row_index + 1][space_index - 1]]}.get(space_index, default)

	def move_checker(self, coordinates_array, mouse_pos, release_space_value, current_checker, first_row_index, first_space_index):
		row_index, space_index = self.get_checker_index(coordinates_array, mouse_pos)
		if release_space_value == 1:
			if current_checker == 3:
				self.board_array[first_row_index][first_space_index] = 1
				self.board_array[row_index][space_index] = 3
			else:
				if current_checker == 2:
					self.board_array[first_row_index][first_space_index] = 1
					self.board_array[row_index][space_index] = 2
				else:
					if current_checker == 4:
						self.board_array[first_row_index][first_space_index] = 1
						self.board_array[row_index][space_index] = 4
					else:
						if current_checker == 5:
							self.board_array[first_row_index][first_space_index] = 1
							self.board_array[row_index][space_index] = 5					


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

	def change_player(self, current_turn, top_player_array, bottom_player_array):
		if current_turn == [3, 5]:
			return top_player_array, bottom_player_array
		else:
			if current_turn == [2, 4]:
				return bottom_player_array, top_player_array


