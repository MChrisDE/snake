import pygame
from constants import BLACK, WHITE


def start_game():
	global run
	run = False

	pygame.init()

	root = fullscreen()
	pygame.display.set_caption("Snake")
	root.fill(WHITE)

	run = True
	while run:
		for event in pygame.event.get():
			print(event)
			if event.type == pygame.QUIT:
				run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					run = False
		pygame.display.update()

	pygame.quit()


def fullscreen():
	# give me the biggest 16-bit display available
	modes = pygame.display.list_modes(16)
	if not modes:
		print('16-bit not supported')
	else:
		return pygame.display.set_mode(modes[0], pygame.FULLSCREEN, 16)
