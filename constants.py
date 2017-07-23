import pygame


class Colors:
	GREY = 50, 50, 50
	WHITE = 255, 255, 255
	BLACK = 0, 0, 0


class Fonts:
	pygame.font.init()
	DEFAULT_FONT40 = pygame.font.SysFont("monospace", 40)  # set after pygame.init()

	@staticmethod
	def default(size):
		return pygame.font.SysFont("monospace", size)


class MoveDirections:
	UP = {pygame.K_UP, pygame.K_w}
	LEFT = {pygame.K_LEFT, pygame.K_a}
	DOWN = {pygame.K_DOWN, pygame.K_s}
	RIGHT = {pygame.K_RIGHT, pygame.K_d}
