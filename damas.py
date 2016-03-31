import pygame, sys, time, clases
from pygame.locals import *

##Initialize 
pygame.init()

window_size = [504, 504]
window_surface = pygame.display.set_mode((window_size),0,32)
pygame.display.set_caption("Damas")
top_checkers_array = []
bottom_checkers_array = []

##Sprites
board_sprite = pygame.image.load("images/checkers_board_8x8.gif")
red_checkers = pygame.image.load("images/ficha_roja_50x50.png")
blue_checkers = pygame.image.load("images/ficha_azul_50x50.png")
red_checkers.set_colorkey((255,255,255),RLEACCEL)
blue_checkers.set_colorkey((255,255,255),RLEACCEL)

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
board = clases.Board(0, 0, board_sprite, blue_checkers, board_array)

top_player = clases.Checker(red_checkers)
bottom_player = clases.Checker(blue_checkers)


## Inicializar tablero para el jugador del top
for y in range(0, 3):
	for x in range(0, 8):
		current_pos = board.initialize(0, 2, "top")
		top_checkers_array.append(current_pos)

## Inicializar tablero para el jugador del bottom
for y in range(0, 3):
	for x in range(0, 8):
		current_pos = board.initialize(5, 3, "bottom")
		bottom_checkers_array.append(current_pos)


##Update loop
while  True:
	window_surface.fill(BGCOLOR)

	#============EVENTS=============
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			pygame.quit()
			sys.exit()

	#============GAME LOGIC=============
	#print board_array
	#print top_checkers_array

	#============DRAW=============
	board.draw(window_surface)
	for checker_pos in top_checkers_array:
		try:
			top_player.draw(window_surface, (checker_pos[0], checker_pos[1]))
		except TypeError:
			pass
	for checker_pos in bottom_checkers_array:
		try:
			bottom_player.draw(window_surface, (checker_pos[0], checker_pos[1]))
		except TypeError:
			pass


	pygame.display.update()
	main_clock.tick(30)
