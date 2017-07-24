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
	NONE = {}

	last_p = None  # last mouse motion position

	@classmethod
	def delta(cls, event):
		p = Position(*event.pos)
		if cls.last_p is None:
			direction = cls.NONE
		else:
			direction = p - cls.last_p
		cls.last_p = p
		return direction


class Position(tuple):
	def __new__(cls, *position, **pos):
		def valid_pos(component):
			isinstance(pos.get(component, None), int)

		if valid_pos('x') and valid_pos('y'):
			seq = pos.get('x'), pos.get('y')
		elif position and len(position) is 2:
			seq = position
		else:
			seq = 0, 0
		return super().__new__(cls, seq)

	def get_x(self):
		return self[0]

	def get_y(self):
		return self[1]

	def __str__(self):
		return ','.join(str(xy) for xy in self)

	def __sub__(self, other):
		if not isinstance(other, type(self)):
			return MoveDirections.NONE
		elif self.get_x() > other.get_x():
			return MoveDirections.RIGHT
		elif self.get_x() < other.get_x():
			return MoveDirections.LEFT
		elif self.get_y() < other.get_y():
			return MoveDirections.UP
		elif self.get_y() > other.get_y():
			return MoveDirections.DOWN
		else:
			return MoveDirections.NONE
