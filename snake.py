from constants import MoveDirections


class Position(tuple):
	is_head = False

	def __init__(self, **position):
		if not position.get('x', False) or not position.get('y', False):
			super().__init__(position.get('position', (0, 0)))
		else:
			super().__init__((position['x'], position['y']))

	def __str__(self):
		return ','.join(str(xy) for xy in self)

	def get_x(self):
		return self[0]

	def get_y(self):
		return self[1]


class Snake(list):
	class Part(Position):
		is_head = False

		def __init__(self, **position):
			super().__init__(**position)

	def __init__(self, root, **initial):
		super().__init__()
		self.length = initial.get('length', 3)
		self.direction = initial.get('direction', MoveDirections.RIGHT)
		self.head_position = initial.get('position', Position())
		self.root = root

		for i in range(self.length):
			self.append(Snake.Part(x=self.head_position[0] - i, y=self.head_position[1]))

	def __str__(self):
		return f'Snake: {";".join([str(part) for part in self])}'
