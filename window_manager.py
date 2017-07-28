from constants import pygame, Colors, Fonts


class Window(dict):
	_instances = []
	_active_instance = None

	class Button:
		def __init__(self, root, text: str = '', x: int = 0, y: int = 0, font=Fonts.DEFAULT_FONT40, fn=lambda: None):
			self.text = font.render(text, True, Colors.BLACK)
			self.rect = self.text.get_rect()
			self.rect.center = (x, y)
			self.root = root
			self.run = fn

		def collidepoint(self, *args) -> bool:
			return self.rect.collidepoint(*args)

		def draw(self):
			self.root.window.blit(self.text, self.rect)

	def __init__(self, dim: tuple = (500, 500), title: str = '', fill: tuple = Colors.WHITE, mode=None, **kwargs):
		super().__init__(**kwargs)
		pygame.init()

		if mode is None:
			mode = pygame.HWSURFACE
		else:
			mode |= pygame.HWSURFACE
		self.window = pygame.display.set_mode(dim, mode)
		pygame.display.set_caption(title)
		self.window.fill(fill)

		self.args = kwargs
		self.args['dim'] = dim
		self.args['title'] = title
		self.args['fill'] = fill
		self.args['mode'] = mode

		if 'id' in kwargs:
			self.id = kwargs['id']
		else:
			self.id = len(Window._instances)
			Window._instances.append(self)

		if not self.get('buttons'):
			self['buttons'] = []
		else:
			for button in self['buttons']:
				button.draw()
		self.set_state(False)

	def set_buttons(self, *mkwargs):
		for kwargs in mkwargs:
			self['buttons'].append(Window.Button(self, **kwargs))
		self.update_display()

	def _get_clicked_button(self) -> Button:
		for button in self['buttons']:
			if button.collidepoint(pygame.mouse.get_pos()):
				return button
		return Window.Button(self)

	def mainloop(self, **fn):
		def handle_quit(ev):
			pass

		def handle_click(ev):
			button = self._get_clicked_button()
			if button is None:
				pass  # No button was clicked or there are no buttons
			else:
				self.set_state(False)
				button.run()

		def handle_key_press(ev):
			if ev.key == pygame.K_ESCAPE:
				self.set_state(False)

		if 'handle_quit' not in fn:
			fn['handle_quit'] = handle_quit
		if 'handle_click' not in fn:
			fn['handle_click'] = handle_click
		if 'handle_key_press' not in fn:
			fn['handle_key_press'] = handle_key_press
		if 'handle_mouse_motion' not in fn:
			fn['handle_mouse_motion'] = handle_quit

		self.set_state(True)

		while self['run']:
			for event in pygame.event.get():
				print(event)
				if event.type == pygame.QUIT:
					self.set_state(False)
					fn['handle_quit'](event)
				elif event.type == pygame.MOUSEBUTTONUP:
					fn['handle_click'](event)
				elif event.type == pygame.KEYDOWN:
					fn['handle_key_press'](event)
				elif event.type == pygame.MOUSEMOTION:
					fn['handle_mouse_motion'](event)

			self.update_display()

	def set_state(self, activate):
		if activate:
			if Window._active_instance is not None:  # allow only one Window to be active
				for window in Window._instances:
					window.set_state(False)

			self.__init__(**self.args)

			Window._active_instance = self.id
			self['run'] = True
			pygame.event.clear()  # Dismiss events from old window
		else:
			Window._active_instance = None
			self['run'] = False

			self.args['id'] = self.id
		# self.args['dim'] = self.window.get_size()

	def get_state(self):
		return self['run']

	def update_display(self):
		if self['run']:
			pygame.display.update()
		else:
			print('This window is not running, we should not update it')

	@classmethod
	def display_window(cls, w_id: int):
		try:
			cls._instances[w_id].set_state(True)
		except IndexError:
			print(f'There is not window with id: {w_id}')

	@staticmethod
	def get_fullscreen(**kwargs):
		pygame.init()

		# give me the biggest 16-bit display available
		modes = pygame.display.list_modes(16)
		if not modes:
			print('16-bit not supported')
			return Window((1280, 720), **kwargs)
		else:
			return Window(modes[0], mode=pygame.FULLSCREEN, depth=16, **kwargs)
