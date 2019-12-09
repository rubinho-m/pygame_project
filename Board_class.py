import pygame


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        left = self.left
        top = self.top
        for __ in range(self.width):
            for _ in range(self.height):
                pygame.draw.rect(screen, pygame.Color('white'), (left, top, self.cell_size, self.cell_size), 1)
                top += self.cell_size
            left += self.cell_size
            top = self.top


pygame.init()
size = w, h = 600, 600
screen = pygame.display.set_mode(size)
running = True
board = Board(4, 3)
board.set_view(100, 100, 50)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    board.render()
    pygame.display.flip()