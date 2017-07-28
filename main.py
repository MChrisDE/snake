from constants import Fonts
from window_manager import Window
from game import start_game

if __name__ == '__main__':
	root = Window(title='Snake Menu')
	root.set_buttons({
		'text': 'Snake',
		'x': 250,
		'y': 100,
		'font': Fonts.default(size=80)
	}, {
		'text': 'Start game',
		'x': 250,
		'y': 250,
		'fn': lambda: start_game(root.id)
	}, {
		'text': 'Exit Game',
		'x': 250,
		'y': 400,
		'fn': exit
	})

	root.mainloop()
