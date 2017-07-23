from snake import start_game
from constants import *

buttons = []


class Button:
	def __init__(self, text, x, y, font=DEFAULT_FONT40, fn=lambda: None):
		self.text = font.render(text, True, BLACK)
		self.rect = self.text.get_rect()
		self.rect.center = (x, y)
		self.run = fn
		root.blit(self.text, self.rect)
		buttons.append(self)

	def collidepoint(self, *args):
		return self.rect.collidepoint(*args)


def create_buttons():
	Button("Snake", 250, 100)
	Button("Start game", 250, 250, fn=start)
	Button("Exit Game", 250, 400, fn=exit_game)

	pygame.display.update()


def exit_game():
	pygame.quit()


def start():
	pygame.quit()
	start_game()


if __name__ == '__main__':
	pygame.init()

	root = pygame.display.set_mode((500, 500))
	pygame.display.set_caption("Snake Menu")
	root.fill(WHITE)

	create_buttons()

	run = True
	while run:
		for event in pygame.event.get():
			print(event)
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONUP:
				for button in buttons:
					if button.collidepoint(pygame.mouse.get_pos()):
						button.run()

		pygame.display.update()

	pygame.quit()
