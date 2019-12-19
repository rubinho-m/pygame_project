import pygame


pygame.init()
size = (width, height) = 500, 500
screen = pygame.display.set_mode(size)
color = ['saddlebrown', 'green']
clock = pygame.time.Clock()

class Board:
    def __init__(self, width, height, cell):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 0
        self.top = 0
        self.cell_size = cell

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for i in range(self.height):
            for j in range(self.width):
                x = self.board[i][j]
                if x == 0:
                    pygame.draw.rect(screen, pygame.Color(color[x]), (self.left + j * self.cell_size,
                                                                      self.top + i * self.cell_size,
                                                                      self.cell_size,
                                                                      self.cell_size))
                else:
                    pygame.draw.rect(screen, pygame.Color(color[x]), (self.left + j * self.cell_size,
                                                                      self.top + i * self.cell_size,
                                                                      self.cell_size,
                                                                      self.cell_size))
                pygame.draw.rect(screen, pygame.Color('black'), (self.left + j * self.cell_size,
                                                                 self.top + i * self.cell_size,
                                                                 self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_pos):
        for i in range(self.height):
            for j in range(self.width):
                x, y = self.left + j * self.cell_size, self.top + i * self.cell_size
                x1, y1 = x + self.cell_size, y + self.cell_size
                if x <= mouse_pos[0] <= x1 and y <= mouse_pos[1] <= y1:
                    return i, j
        return None

    def on_click(self, cell_coords):
        i, j = cell_coords
        self.board[i][j] ^= 1

    def process_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            self.on_click(cell)

fps = 10
board = Board(17, 17, 30)
board.render()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(fps)
    pygame.display.flip()

pygame.quit()