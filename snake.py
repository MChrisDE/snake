from constants import pygame, MoveDirections, Position, Colors
import window_manager


class Snake(list):
	default_width = 16
	default_border = 1
	default_length = 3
	default_color = Colors.WHITE
	default_direction =  MoveDirections.DIRECTION['RIGHT']

	class Part(Position):
		is_head = False

		def __new__(cls, *position, **pos):
			return super().__new__(cls, *position, **pos)

		def __init__(self, parent=None, *position, **pos):
			super().__init__()
			size = parent.size if isinstance(parent, Snake) else Snake.default_width
			self.rect = pygame.Rect(self.get_x(), self.get_y(), self.get_x() + size, self.get_y() + size)

			self.is_head = pos.get('head', False)

		def __str__(self):
			return str(self.get_x()) + ',' + str(self.get_y())

		def get_rect(self, x_offset=0, y_offset=0):
			self.rect.move_ip(x=x_offset, y=y_offset)

	def __init__(self, root: window_manager.Window, **initial):
		"""
		:param root: the window to draw the snake on
		:param initial: position, length, direction, size, color, border
		"""
		super().__init__()
		self.length = initial.get('length', Snake.default_length)
		self.direction = initial.get('direction', Snake.default_direction)
		self.size = initial.get('size', Snake.default_width)
		self.color = initial.get('color', Snake.default_color)
		self.border = initial.get('border', Snake.default_border)
		self.root = root

		head_position = initial.get('position', (0, 0))

		self.append(Snake.Part(*head_position, head=True))
		for i in range(1, self.length):
			self.append(Snake.Part(head_position[0] - i * (self.size + self.border), head_position[1]))

	def draw(self):
		for part in self:
			pygame.draw.rect(self.root.window, self.color, part.rect)
		# self.root.window.blit(self.root.window, part.rect)

	def __str__(self):
		return f'Snake: {";".join(map(str, self))}'
