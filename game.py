from constants import *
from snake import Snake


def start_game():
	global run
	run = False

	pygame.init()

	root = fullscreen()
	pygame.display.set_caption("Snake")
	root.fill(Colors.GREY)
	snake = Snake(root)
	print(snake)

	run = True
	while run:
		for event in pygame.event.get():
			print(event)
			if event.type == pygame.QUIT:
				run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					run = False
				elif event.key in MoveDirections.UP:
					print('Snake move up')
				elif event.key in MoveDirections.LEFT:
					print('Snake move left')
				elif event.key in MoveDirections.DOWN:
					print('Snake move down')
				elif event.key in MoveDirections.RIGHT:
					print('Snake move right')

		pygame.display.update()

	pygame.quit()


def fullscreen():
	# give me the biggest 16-bit display available
	modes = pygame.display.list_modes(16)
	if not modes:
		print('16-bit not supported')
		return pygame.display.set_mode((1280, 720))
	else:
		return pygame.display.set_mode(modes[0], pygame.FULLSCREEN, 16)
