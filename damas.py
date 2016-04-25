import pygame, sys, time, board, checker
from pygame.locals import *

##Initialize 
pygame.init()

window_size = [704, 504]
window_surface = pygame.display.set_mode((window_size),0,32)
pygame.display.set_caption("Damas")
current_row = 0
check_selected = False
next_pos = []
sprites_dict = {}
top_player_array = []
bottom_player_array = []
trigger_wrong_label = False
wrong_label_pos_x, wrong_label_pos_y = 152, 252


##Sprites
board_sprite = pygame.image.load("images/checkers_board_8x8.gif")
red_checkers = pygame.image.load("images/ficha_roja_50x50.png")
blue_checkers = pygame.image.load("images/ficha_azul_50x50.png")
red_checkers_alpha = pygame.image.load("images/ficha_roja_50x50.png")
blue_checkers_alpha = pygame.image.load("images/ficha_azul_50x50.png")
background = pygame.image.load("images/background01.jpg")

red_checkers.set_colorkey((255,255,255),RLEACCEL)
red_checkers_alpha.set_colorkey((255,255,255),RLEACCEL)
blue_checkers.set_colorkey((255,255,255),RLEACCEL)
blue_checkers_alpha.set_colorkey((255,255,255),RLEACCEL)
red_checkers_alpha.set_alpha(80)
blue_checkers_alpha.set_alpha(80)
background.set_colorkey()

sprites_dict = {
	"top_player": {"sprite": red_checkers, "alpha_sprite": red_checkers_alpha},
	"bottom_player": {"sprite": blue_checkers, "alpha_sprite": blue_checkers_alpha}
}

##Font and Text
myfont = pygame.font.Font(None, 36)
label = myfont.render("Player Turn:", 1, (255, 255, 0))
wrong_label = myfont.render("Not your turn yet!", 1, (255, 125, 50))


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
board = board.Board(0, 0, board_sprite, board_array)

#top_player = checker.Checker(sprites_dict, "top_player")
bottom_player = checker.Checker(sprites_dict, "bottom_player")

## Inicializar tablero para el jugador del top
board.initialize(0, 2)
## Inicializar tablero para el jugador del bottom
board.initialize(5, 3)
## Calcular coordenadas de cada espacio del tablero
coordinates_array = board.get_coordinates()
##Inicializar turno, jugador bottom primero
current_turn = board.init_turn("bottom")

for row in board_array:
	for space in row:
		if space == 2:
			top_player = checker.Checker(sprites_dict, "top_player")
			top_player_array.append(top_player)
		else:
			if space == 3:
				bottom_player = checker.Checker(sprites_dict, "bottom_player")
				bottom_player_array.append(bottom_player)

## Inicializar posicion de los rects de las fichas
current_row = 0
top_checker_index = 0
bot_checker_index = 0
for row in board_array:
		current_space = 0
		for space in row:
			if space == 2 or space == 4:
					top_player_array[top_checker_index].new_pos(coordinates_array[current_row][current_space])
					top_checker_index+= 1
			if space == 3 or space == 5:
				bottom_player_array[bot_checker_index].new_pos(coordinates_array[current_row][current_space])

				bot_checker_index+= 1
			current_space += 1
		current_row += 1 

current_player_array = bottom_player_array
current_enemy_array = top_player_array

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

		if event.type == MOUSEBUTTONDOWN:
			first_row_index, first_space_index = board.get_checker_index(coordinates_array, pygame.mouse.get_pos())
			space_value = board.get_space_value(first_row_index, first_space_index)
			next_pos = [(0,0)]
			current_coordinate = board.get_space_coordinates(coordinates_array, first_row_index, first_space_index)

			for checker in current_player_array:
				if checker.get_coordinates() == current_coordinate:
					current_index = current_player_array.index(checker)

			for checker in current_enemy_array:
				if checker.sprite_rect.collidepoint(event.pos):
					wrong_label_pos_x, wrong_label_pos_y = pygame.mouse.get_pos()[0] - 100, pygame.mouse.get_pos()[1]
					wrong_label = myfont.render("Not your turn yet!", 1, (255, 125, 50))
					label_time = 20
					trigger_wrong_label = True


			try:		
				if current_player_array[current_index].sprite_rect.collidepoint(event.pos) and space_value in current_turn:
					check_selected = True
					next_coordinates = board.get_next_row_coordinates(coordinates_array, space_value, first_row_index, first_space_index)
					print next_coordinates
					positions = board.get_next_pos(coordinates_array, next_coordinates, space_value, current_coordinate)
					next_pos = positions["next_pos"]
					enemy_pos = positions["enemy_pos"]
			except NameError:
				wrong_label_pos_x, wrong_label_pos_y = pygame.mouse.get_pos()[0] - 100, pygame.mouse.get_pos()[1]
				wrong_label = myfont.render("Pick a blue checker", 1, (255, 125, 50))
				label_time = 20
				trigger_wrong_label = True


		if event.type == MOUSEBUTTONUP:
			if pygame.mouse.get_pos()[0] < board.get_board_width():
				second_row_index, second_space_index = board.get_checker_index(coordinates_array, pygame.mouse.get_pos())
				release_space_value = board.get_space_value(second_row_index, second_space_index)
				release_pos = board.get_space_coordinates(coordinates_array, second_row_index, second_space_index)
				print release_pos

				if release_pos in next_pos and release_space_value == 1:
					current_player_array[current_index].new_pos(release_pos)
					board.move_checker(coordinates_array, pygame.mouse.get_pos(), release_space_value, space_value, first_row_index, first_space_index)
					
					## Revisar si hay fichas que se puedan comer
					if release_pos not in next_coordinates:
						next_coordinates = board.get_next_row_coordinates(coordinates_array, space_value, second_row_index, second_space_index)
						positions = board.get_next_pos(coordinates_array, next_coordinates, space_value, release_pos)
						next_pos = positions["next_pos"]
						next_enemy_pos = positions["enemy_pos"]
						for checker in current_enemy_array:
							for pos in enemy_pos:
								try:
									if checker.get_coordinates() == pos:
										current_enemy_array.remove(checker)
										enemy_coord_index = board.get_coord_index(coordinates_array, [pos])
										board_array[enemy_coord_index[0][0]][enemy_coord_index[0][1]] = 1
										if (len(next_pos) == 0) or (len(next_pos) == 1 and next_pos[0][1] == next_enemy_pos[0][1]) or (len(next_pos) == 2 and next_enemy_pos == []):
											current_player_array, current_enemy_array = board.change_player(current_turn, top_player_array, bottom_player_array)
											current_turn = board.change_turn(current_turn)
										break
								except ValueError:
									pass
					else:
						current_player_array, current_enemy_array = board.change_player(current_turn, top_player_array, bottom_player_array)
						current_turn = board.change_turn(current_turn)
				check_selected = False
			else:
				check_selected = False


	#============DRAW=============
	window_surface.blit(background, (0,0))
	board.draw(window_surface)
	window_surface.blit(label, (540, 216))

	if current_turn == [2, 4]:
		top_player.draw_current_turn(window_surface)
	else:
		bottom_player.draw_current_turn(window_surface)

	if len(bottom_player_array) > 0 or len(top_player_array) > 0:
		for checker in bottom_player_array:
			checker.draw(window_surface)

		for checker in top_player_array:
			checker.draw(window_surface)
	else:
		label = myfont.render("Game Over!", 1, (255, 255, 0))

	if check_selected:
		current_player_array[current_index].draw_on_cursor(window_surface, pygame.mouse.get_pos())
		for pos in next_pos:
			if board.get_space_value(first_row_index, first_space_index) == 3: 
				bottom_player.draw_on_next_row(window_surface, (pos[0], pos[1]))
			else:
				top_player.draw_on_next_row(window_surface,(pos[0],pos[1]))



	if trigger_wrong_label:
		label_time -= 1
		window_surface.blit(wrong_label, (wrong_label_pos_x, wrong_label_pos_y))
		wrong_label_pos_y -= 1
		if label_time == 0:
			trigger_wrong_label = False

	pygame.display.update()
	main_clock.tick(30)
