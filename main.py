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

FPS = 30


def load_level(filename):
    filename = "levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Player(pygame.sprite.Sprite):

    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(player_sprite)
        sheet = pygame.transform.scale(sheet, (500, 400))
        self.scale = 90
        self.rotate = False
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.idle = load_image("grass.png", -1)
        self.idle = pygame.transform.scale(self.idle, (self.scale, self.scale))
        self.rect = self.rect.move(x, y)
        self.state = True

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                if i != columns - 1:
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        if self.state:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        else:
            if self.rotate:
                self.image = pygame.transform.flip(self.image, True, False)
            self.image = self.idle


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
    # new_player = Player(load_image("player_anim.png", -1), 7, 4, 0, 0)
    # elif level[y][x] == '@':
    #     Earth('empty', x, y)
    #     new_player = Player(x, y)
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Эра динозавров", "",
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
                print(1)
                return False
        pygame.display.flip()
        clock.tick(FPS)


def start_main():
    # board = Board(15, 12, 70)
    # board.render()
    player = Player(load_image("player_anim.png", -1), 7, 4, 0, 0)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            player.rotate = False
            player.rect.x += 10
            player_sprite.update()
        if keys[pygame.K_LEFT]:
            player.rotate = True
            player.rect.x -= 10
            player_sprite.update()
            player.image = pygame.transform.flip(player.image, True, False)
        if keys[pygame.K_UP]:
            player.rect.y -= 10
            player_sprite.update()
        if keys[pygame.K_DOWN]:
            player.rect.y += 10
            player_sprite.update()
        if not keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            player.state = False
        else:
            player.state = True
        all_sprites.update()
        volcano_group.update()

        # screen.fill(pygame.Color('black'))

        all_sprites.draw(screen)
        volcano_group.draw(screen)
        player_sprite.draw(screen)
        player_sprite.update()
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()


tile_images = {'volcano': load_image('volcano.png'), 'empty': load_image('earth.jpg')}

all_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
volcano_group = pygame.sprite.Group()

player, x, y = generate_level(load_level('first.txt'))
if not start_screen():
    start_main()
