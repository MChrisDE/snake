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
	UP = {'UP', pygame.K_UP, pygame.K_w}
	LEFT = {'LEFT', pygame.K_LEFT, pygame.K_a}
	DOWN = {'DOWN', pygame.K_DOWN, pygame.K_s}
	RIGHT = {'RIGHT', pygame.K_RIGHT, pygame.K_d}
	NONE = {}

	last_direction = last_event = None

	@classmethod
	def get_direction(cls, event) -> set:
		# This method may be called multiple times on the same event
		# in this case we return the last direction

		if event is cls.last_event:  # return immediately
			return cls.last_direction
		elif cls.last_event is None:
			cls.last_event = event

		new_pos, old_pos = Position(*event.pos), Position(*cls.last_event.pos)
		cls.last_direction = new_pos.determine_movement_direction(old_pos)
		return cls.last_direction


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

	def determine_movement_direction(self, other):
		def horizontal_movement():
			if self.get_x() > other.get_x():
				return MoveDirections.RIGHT
			elif self.get_x() < other.get_x():
				return MoveDirections.LEFT

		def vertical_movement():
			if self.get_y() < other.get_y():
				return MoveDirections.UP
			elif self.get_y() > other.get_y():
				return MoveDirections.DOWN

		horizontal_distance = abs(self.get_x() - other.get_x())
		vertical_distance = abs(self.get_y() - other.get_y())

		if not isinstance(other, type(self)):
			return MoveDirections.NONE
		elif horizontal_distance > vertical_distance:
			return horizontal_movement()
		elif horizontal_distance < vertical_distance:
			return vertical_movement()
		# this is a tricky situation (= RNG time)
		# rather return MoveDirection.NONE for a distance equal to 0
		elif horizontal_distance == vertical_distance and vertical_distance is not 0:
			import random
			return random.choice((horizontal_movement, vertical_movement))()
		else:
			return MoveDirections.NONE
