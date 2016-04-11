import pygame, sys, time, board, checker
from pygame.locals import *

##Initialize 
pygame.init()

window_size = [504, 504]
window_surface = pygame.display.set_mode((window_size),0,32)
pygame.display.set_caption("Damas")
current_row = 0
check_selected = False
next_pos = []
sprites_dict = {}
top_player_array = []
bottom_player_array = []


##Sprites
board_sprite = pygame.image.load("images/checkers_board_8x8.gif")
red_checkers = pygame.image.load("images/ficha_roja_50x50.png")
blue_checkers = pygame.image.load("images/ficha_azul_50x50.png")
red_checkers_alpha = pygame.image.load("images/ficha_roja_50x50.png")
blue_checkers_alpha = pygame.image.load("images/ficha_azul_50x50.png")

red_checkers.set_colorkey((255,255,255),RLEACCEL)
red_checkers_alpha.set_colorkey((255,255,255),RLEACCEL)
blue_checkers.set_colorkey((255,255,255),RLEACCEL)
blue_checkers_alpha.set_colorkey((255,255,255),RLEACCEL)
red_checkers_alpha.set_alpha(80)
blue_checkers_alpha.set_alpha(80)

red_checkers_rect = red_checkers.get_rect()
blue_checkers_rect = blue_checkers.get_rect()
sprites_dict = {
	"top_player": {"sprite": red_checkers, "alpha_sprite": red_checkers_alpha},
	"bottom_player": {"sprite": blue_checkers, "alpha_sprite": blue_checkers_alpha}
}
##How fast the screen updates
main_clock = pygame.time.Clock()

##BG color
BGCOLOR = (0, 0, 0)

# 0 = espacio vacio no jugable, 1 = espacio vacio jugable
# 2 = ficha top, 3 = ficha bottom, 4= dama top, 5= dama bottom
board_array = [[0,1,0,1,0,1,0,1],
				[1,0,1,0,1,0,1,0]]
for unused in range(0, 3):
	board_array.append([0,1,0,1,0,1,0,1])
	board_array.append([1,0,1,0,1,0,1,0])


##Objects
board = board.Board(0, 0, board_sprite, blue_checkers, board_array)

#top_player = checker.Checker(sprites_dict, "top_player")
bottom_player = checker.Checker(sprites_dict, "bottom_player")

## Inicializar tablero para el jugador del top
board.initialize(0, 2)
## Inicializar tablero para el jugador del bottom
board.initialize(5, 3)
## Calcular coordenadas de cada espacio del tablero
coordinates_array = board.get_coordinates()

for row in board_array:
	for space in row:
		if space == 2:
			top_player = checker.Checker(sprites_dict, "top_player")
			top_player_array.append(top_player)
		else:
			if space == 3:
				bottom_player = checker.Checker(sprites_dict, "bottom_player")
				bottom_player_array.append(bottom_player)

#board_array[2][1] = 3
print board_array
print coordinates_array

##Update loop
while  True:
	window_surface.fill(BGCOLOR)

	#============EVENTS=============
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			pygame.quit()
			sys.exit()

		if event.type == MOUSEMOTION:
			pos = event.pos
			for player in top_player_array:
				if player.sprite_rect.collidepoint(pos):
					checker_index = top_player_array.index(player)

		if event.type == MOUSEBUTTONDOWN:		
			first_row_index, first_space_index = board.get_checker_index(coordinates_array, pygame.mouse.get_pos())
			space_value = board.get_space_value(first_row_index, first_space_index)
			if space_value != 0 and space_value != 1:
				check_selected = True
				next_pos = board.get_next_row_coordinates(coordinates_array, space_value, first_row_index, first_space_index)
				print next_pos
				#board.check_next_row()

		if event.type == MOUSEBUTTONUP:
			second_row_index, second_space_index = board.get_checker_index(coordinates_array, pygame.mouse.get_pos())
			release_space_value = board.get_space_value(second_row_index, second_space_index)
			release_pos = board.get_space_coordinates(coordinates_array, second_row_index, second_space_index)
			print release_pos
			if [release_pos] in next_pos:
				board.move_checker(coordinates_array, pygame.mouse.get_pos(), release_space_value, space_value, checker_index, first_row_index, first_space_index)
			check_selected = False
			print len(top_player_array)


	#============GAME LOGIC=============
	#print board_array
	#print top_checkers_array
	#print pygame.mouse.get_pos()

	#============DRAW=============
	board.draw(window_surface)
	if len(top_player_array) > 0:
		current_row = 0
		top_checker_index = 0
		bot_checker_index = 0
		for row in board_array:
			current_space = 0
			for space in row:
				if space == 2 or space == 4:
						top_player_array[top_checker_index].draw(window_surface,(coordinates_array[current_row][current_space]))
						top_checker_index+= 1
				if space == 3 or space == 5:
					bottom_player_array[bot_checker_index].draw(window_surface,(coordinates_array[current_row][current_space]))
					bot_checker_index+= 1
				current_space += 1
			current_row += 1 

	if check_selected:
		for space in next_pos:
			for pos in space:
				if board.get_space_value(first_row_index, first_space_index) == 3: ##Para tomar en cuenta el turno
					bottom_player.draw_on_next_row(window_surface, (pos[0], pos[1]))
				else:
					top_player.draw_on_next_row(window_surface,(pos[0],pos[1]))

	pygame.display.update()
	main_clock.tick(30)
