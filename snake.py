from constants import MoveDirections, Position


class Snake(list):
	class Part(Position):
		is_head = False

		def __new__(cls, *position, **pos):
			return super().__new__(cls, *position, **pos)

		def __init__(self, *position, **pos):
			super().__init__()

			if 'head' in pos:
				self.is_head = pos['head']
				del pos['head']

		def __str__(self):
			return str(self.get_x()) + ',' + str(self.get_y())

	def __init__(self, root, **initial):
		super().__init__()
		self.length = initial.get('length', 3)
		self.direction = initial.get('direction', MoveDirections.DIRECTION['RIGHT'])
		self.head_position = initial.get('position', Snake.Part(head=True))
		self.root = root

		self.append(self.head_position)
		for i in range(1, self.length):
			self.append(Snake.Part(self.head_position.get_y() - i, self.head_position.get_y()))

	def __str__(self):
		return f'Snake: {";".join(map(str, self))}'
