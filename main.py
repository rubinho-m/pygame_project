import pygame
import os
import sys
from Board_class import Board
from Volcano_class import Volcano
from Earth_class import Earth

pygame.init()
size = (width, height) = 800, 600
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('black'))
clock = pygame.time.Clock()

FPS = 10


def load_level(filename):
    filename = "levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

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

def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            Earth('empty', x, y, all_sprites)
            if level[y][x] == '#':
                Volcano('volcano', x, y, volcano_group, all_sprites)
# здесь должен появитьтся спрайт с игроком
            # elif level[y][x] == '@':
            #     Earth('empty', x, y)
            #     new_player = Player(x, y)
    return new_player, x, y

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
    # board = Board(15, 12, 70)
    # board.render()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.update()
        volcano_group.update()

        screen.fill(pygame.Color('black'))

        all_sprites.draw(screen)
        volcano_group.draw(screen)
        clock.tick(10)
        pygame.display.flip()

    pygame.quit()


tile_images = {'volcano': load_image('volcano.png'), 'empty': load_image('earth.jpg')}

all_sprites = pygame.sprite.Group()
volcano_group = pygame.sprite.Group()

player, x, y = generate_level(load_level('first.txt'))
if not start_screen():
    start_main()

