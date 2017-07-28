from constants import pygame, MoveDirections, Colors
from snake import Snake
from window_manager import Window

DIRECTION = MoveDirections.DIRECTION
get_direction = MoveDirections.get_direction


def start_game(menu_id: int):
	root = Window.get_fullscreen(title='Snake', fill=Colors.GREY)
	root['snake'] = Snake(root)
	print(root['snake'])

	def handle_key_press(event):
		if event.key == pygame.K_ESCAPE:
			root.set_state(False)
		elif event.key in DIRECTION['UP']:
			print('Snake move up')
		elif event.key in DIRECTION['LEFT']:
			print('Snake move left')
		elif event.key in DIRECTION['DOWN']:
			print('Snake move down')
		elif event.key in DIRECTION['RIGHT']:
			print('Snake move right')

	def handle_mouse_motion(event):
		if get_direction(event) is not DIRECTION['NONE']:
			if get_direction(event) is DIRECTION['UP']:
				print('Snake move up')
			elif get_direction(event) is DIRECTION['LEFT']:
				print('Snake move left')
			elif get_direction(event) is DIRECTION['DOWN']:
				print('Snake move down')
			elif get_direction(event) is DIRECTION['RIGHT']:
				print('Snake move right')

	def handle_quit(event):
		Window.display_window(menu_id)

	root.mainloop(handle_quit=handle_quit, handle_key_press=handle_key_press, handle_mouse_motion=handle_mouse_motion)
