from constants import Colors, Fonts, pygame, DEFAULT_RES


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

	class Clock:
		def __init__(self):
			self.clock = pygame.time.Clock()
			self.max_fps = self.total_ticks = 0

		def tick(self):
			self.total_ticks += 1
			self.clock.tick(self.max_fps)
			return f'Tick {self.total_ticks}, FPS {self.get_fps()}'

		def set_max_fps(self, max_fps):
			self.max_fps = max_fps

		def get_fps(self):
			return self.clock.get_fps()

	def __new__(cls, dim: tuple = (500, 500), **kwargs):
		kwargs['dim'] = dim
		self = dict.__new__(cls, **kwargs)  # well, it magically works...

		self.id = len(Window._instances)
		Window._instances.append(self)
		self['buttons'] = []
		self.clock = Window.Clock()

		def on_click(ev):
			button = self._get_clicked_button()
			if button is None:
				pass  # No button was clicked or there are no buttons
			else:
				self.set_state(False)
				button.run()

		def on_key_press(ev):
			if ev.key == pygame.K_ESCAPE:
				self.set_state(False)

		on_mouse_motion = on_all_events_handled = on_quit = lambda *ev: None
		self.fn = {
			'on_quit': kwargs.get('on_quit', on_quit),
			'on_click': kwargs.get('on_click', on_click),
			'on_key_press': kwargs.get('on_key_press', on_key_press),
			'on_mouse_motion': kwargs.get('on_mouse_motion', on_mouse_motion),
			'on_all_events_handled': kwargs.get('on_all_events_handled', on_all_events_handled)
		}

		self.args = kwargs  # save the args for reconstruction
		return self

	def __init__(self, dim: tuple = (500, 500), title: str = '', fill: tuple = Colors.WHITE, mode: int = None,
			max_fps=60, *args, **kwargs):
		super().__init__(**kwargs)
		pygame.init()

		if mode is None:
			mode = pygame.HWSURFACE
		else:
			mode |= pygame.HWSURFACE | pygame.DOUBLEBUF
		self.window = pygame.display.set_mode(dim, mode)
		pygame.display.set_caption(title)
		self.window.fill(fill)
		self.clock.set_max_fps(max_fps)

		for button in self['buttons']:
			button.draw()

		self.set_state(False)

	def set_buttons(self, *mkwargs):
		for kwargs in mkwargs:
			self['buttons'].append(Window.Button(self, **kwargs))

	def _get_clicked_button(self) -> Button:
		for button in self['buttons']:
			if button.collidepoint(pygame.mouse.get_pos()):
				return button

	def mainloop(self, **fn):
		self.fn.update(fn)
		self.set_state(True)

		while self.get_state():
			for event in pygame.event.get():
				print(event)
				if event.type == pygame.QUIT or not self.get_state():
					self.set_state(False)
					self.fn['on_quit'](event)
				elif event.type == pygame.MOUSEBUTTONUP:
					self.fn['on_click'](event)
				elif event.type == pygame.KEYDOWN:
					self.fn['on_key_press'](event)
				elif event.type == pygame.MOUSEMOTION:
					self.fn['on_mouse_motion'](event)

			self.fn['on_all_events_handled']()
			print(self.clock.tick())
			pygame.display.update()

	def set_state(self, should_activate: bool, kill: bool = False):
		"""
		Activate or deactivate a window, depending on the value of should_activate
		Note: It is not possible to have more than one window active at any given moment!

		:param kill: Kill the window instance
		:param should_activate: True: activate window, False: deactivate it
		"""
		if should_activate:
			if Window._active_instance is not None:  # allow only one Window to be active
				Window.get_active_window().set_state(False)  # Forcefully 'close' window

			self.__init__(**self.args)  # reconstruct the window

			Window._active_instance = self.id
			self['run'] = True
			pygame.event.clear()  # Dismiss events from old window
		else:
			Window._active_instance = None
			self['run'] = False

			self.args['id'] = self.id
			# self.args['dim'] = self.window.get_size() # if the window was resized
			if kill:
				del Window._instances[self.id]

	def get_state(self):
		return self['run']

	@classmethod
	def get_active_window(cls):
		try:
			return cls._instances[cls._active_instance]
		except (IndexError, TypeError):  # IndexError <= This should never happen!
			print('There is no active window')

	@classmethod
	def _get_window(cls, w_id: int):
		try:
			return cls._instances[w_id]
		except IndexError:
			print(f'There is not window with id: {w_id}')

	@classmethod
	def display_window(cls, w_id: int):
		cls._get_window(w_id).mainloop()

	@staticmethod
	def get_fullscreen(**kwargs):
		"""
		Create a fullscreen Window with the highest supported resolution

		:param kwargs: Are passed to the Window()
		:return: the fullscreen Window
		"""
		return Window(DEFAULT_RES, mode=pygame.FULLSCREEN, **kwargs)
