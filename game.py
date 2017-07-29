from constants import pygame, MoveDirections, Colors
from snake import Snake
from window_manager import Window

DIRECTION = MoveDirections.DIRECTION
get_direction = MoveDirections.get_direction


def start_game(menu_id: int):
	def on_key_press(event):
		if event.key == pygame.K_ESCAPE:
			on_quit(event)
		elif event.key in DIRECTION['UP']:
			print('Snake move up')
		elif event.key in DIRECTION['LEFT']:
			print('Snake move left')
		elif event.key in DIRECTION['DOWN']:
			print('Snake move down')
		elif event.key in DIRECTION['RIGHT']:
			print('Snake move right')

	def on_mouse_motion(event):
		if get_direction(event) is not DIRECTION['NONE']:
			if get_direction(event) is DIRECTION['UP']:
				print('Snake move up')
			elif get_direction(event) is DIRECTION['LEFT']:
				print('Snake move left')
			elif get_direction(event) is DIRECTION['DOWN']:
				print('Snake move down')
			elif get_direction(event) is DIRECTION['RIGHT']:
				print('Snake move right')

	def on_quit(event):
		# root.set_state(False, kill=True)
		Window.display_window(menu_id)  # use the id to get main menu window

	def on_all_events_handled():
		root['snake'].draw()

	root = Window.get_fullscreen(title='Snake', fill=Colors.GREY, max_fps=20, on_quit=on_quit,
			on_key_press=on_key_press, on_mouse_motion=on_mouse_motion, on_all_events_handled=on_all_events_handled)
	root['snake'] = Snake(root, position=(5, 5))
	print(root['snake'])

	root.mainloop()
