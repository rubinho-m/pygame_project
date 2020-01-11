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
        self.flag = 1

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        left = self.left
        top = self.top
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, pygame.Color('white'),
                                 (left, top, self.cell_size, self.cell_size), 1)
                if self.board[j][i] == 1:
                    pygame.draw.line(screen, pygame.Color('blue'), (left, top),
                                     (left + self.cell_size, top + self.cell_size))
                    pygame.draw.line(screen, pygame.Color('blue'), (left + self.cell_size, top),
                                     (left, top + self.cell_size))
                elif self.board[j][i] == 2:
                    pygame.draw.circle(screen, pygame.Color('red'),
                                       (left + self.cell_size // 2, top + self.cell_size // 2),
                                       self.cell_size // 2 - 2, 2)
                top += self.cell_size
            left += self.cell_size
            top = self.top

    def get_cell(self, mouse_pos):
        x = (mouse_pos[0] - self.left) // self.cell_size
        y = (mouse_pos[1] - self.top) // self.cell_size
        if 0 < x + 1 <= self.width and 0 < y + 1 <= self.height:
            return x, y
        return None

    def on_click(self, cell_coords):
        if cell_coords is not None:
            x = cell_coords[0]
            y = cell_coords[1]
            if self.board[y][x] == 0 and self.flag == 1:
                self.board[y][x] = 1
            elif self.board[y][x] == 0 and self.flag == 0:
                self.board[y][x] = 2
            if self.flag == 1:
                self.flag = 0
            else:
                self.flag = 1

        self.render()

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


pygame.init()
size = w, h = 300, 300
screen = pygame.display.set_mode(size)
running = True
board = Board(5, 5)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    screen.fill((0, 0, 0))
    board.render()
    pygame.display.flip()
