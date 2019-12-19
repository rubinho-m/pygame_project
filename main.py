import pygame
import os
import sys
from Board_class import Board

pygame.init()
size = (width, height) = 800, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

FPS = 10


def load_image(name, color_key=None):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image

def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Ера динозавров", "",
                  "Вы попали в джунгли Юрского периода,",
                  "и Вам предстоит добраться до своего",
                  "реактивного самолёта, минуя динозавров",
                  "и избегая ударов метеоритов.",
                  'Будьте осторожны и внимательны:',
                  'дорога таит в себе много опасностей! ']

    fon = pygame.transform.scale(load_image('start_dino.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    line = intro_text[0]
    string_rendered = font.render(line, 6, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    text_coord = 50
    intro_rect.top = text_coord
    intro_rect.x = 310
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)
    text_coord = 60
    for line in intro_text[1:]:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 200
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return False
        pygame.display.flip()
        clock.tick(FPS)

def start_main():
    board = Board(15, 12, 70)
    board.render()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(10)
        pygame.display.flip()

    pygame.quit()

if not start_screen():
    start_main()

