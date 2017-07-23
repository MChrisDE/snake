from constants import MoveDirections


class Position(tuple):
	is_head = False

	def __new__(cls, *position, **pos):
		if not pos.get('x', True) and not pos.get('y', True):
			seq = pos.get('x'), pos.get('y')
		elif position and len(position) is 2:
			seq = position
		else:
			seq = 0, 0
		return super().__new__(cls, seq)

	def __str__(self):
		return ','.join(str(xy) for xy in self)

	def get_x(self):
		return self[0]

	def get_y(self):
		return self[1]


class Snake(list):
	class Part(Position):
		is_head = False

		def __new__(cls, *position, **pos):
			return super().__new__(cls, *position, **pos)

	def __init__(self, root, **initial):
		super().__init__()
		self.length = initial.get('length', 3)
		self.direction = initial.get('direction', MoveDirections.RIGHT)
		self.head_position = initial.get('position', Snake.Part())
		self.root = root

		self.append(self.head_position)
		for i in range(1, self.length):
			self.append(Snake.Part(self.head_position.get_y() - i, self.head_position.get_y()))

	def __str__(self):
		return f'Snake: {";".join([str(part) for part in self])}'
