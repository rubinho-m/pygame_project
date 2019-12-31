import pygame
import os
import sys
from Board_class import Board
from Volcano_class import Volcano
from Earth_class import Earth
from anim_sprite import Player
from buttons import Button
from Plane_class import Plane
from Dino_class import Dino
from FireBall_class import FireBall

pygame.init()
size = (width, height) = 800, 600
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('black'))
clock = pygame.time.Clock()

FPS = 25


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

            elif level[y][x] == '@':
                new_player = Player(player_sprite, load_image("player_anim.png", -1), 7, 4, x * 70,
                                    y * 60)
                pos_x, pos_y = x, y

            elif level[y][x] == 'P':
                plane = Plane('plane', x * 70, y * 60, plane_group, all_sprites)
    # второй цикл добавляет динозавров на поле с определением движения пламени
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'D':
                vect = count_space(x, y)
                Dino(x, y, vect, dino_group, all_sprites)
                FireBall(x * 70, y * 60, vect, fire_group, all_sprites)
    return new_player, pos_x, pos_y, plane


def count_space(x, y):
    kr, kl, ku, kd = 0, 0, 0, 0
    for xx in range(x - 1, -1, -1):
        spr = Volcano('volcano', xx, y)
        if pygame.sprite.spritecollideany(spr, volcano_group, False):
            break
        kl += 1
    for xx in range(x + 1, len(load_level('first.txt')[0])):
        spr = Volcano('volcano', xx, y)
        if pygame.sprite.spritecollideany(spr, volcano_group, False):
            break
        kr += 1
    for yy in range(y - 1, -1, -1):
        spr = Volcano('volcano', x, yy)
        if pygame.sprite.spritecollideany(spr, volcano_group, False):
            break
        kd += 1
    for yy in range(y + 1, len(load_level('first.txt'))):
        spr = Volcano('volcano', x, yy)
        if pygame.sprite.spritecollideany(spr, volcano_group, False):
            break
        ku += 1

    mx = max(ku, kd, kr, kl)
    if mx == ku:
        return (0, ku)
    elif mx == kd:
        return (0, -kd)
    elif mx == kl:
        return (-kl, 0)
    else:
        return (kr, 0)


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
                return MENU
        pygame.display.flip()
        clock.tick(FPS)


def start_main():
    player.rect.w = player.player_scale
    player.rect.h = player.player_scale
    step = 5
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            player.rotate = False
            player.rect.x += step
            player_sprite.update()
            collide = pygame.sprite.groupcollide(player_sprite, volcano_group, False, False)
            if len(collide) != 0:
                player.rect.x -= step
        if keys[pygame.K_LEFT]:
            player.rotate = True
            player.rect.x -= step
            player_sprite.update()
            player.image = pygame.transform.flip(player.image, True, False)
            collide = pygame.sprite.groupcollide(player_sprite, volcano_group, False, False)
            if len(collide) != 0:
                player.rect.x += step

        if keys[pygame.K_UP]:
            player.rect.y -= step
            player_sprite.update()
            collide = pygame.sprite.groupcollide(player_sprite, volcano_group, False, False)
            if len(collide) != 0:
                player.rect.y += step
        if keys[pygame.K_DOWN]:
            player.rect.y += step
            player_sprite.update()
            collide = pygame.sprite.groupcollide(player_sprite, volcano_group, False, False)
            if len(collide) != 0:
                player.rect.y -= step
        if not keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_LEFT] and not \
                keys[pygame.K_RIGHT]:
            player.state = False
        else:
            player.state = True

        for fire in fire_group:
            if pygame.sprite.spritecollideany(fire, volcano_group, False):
                fire.return_back()

        all_sprites.update()
        volcano_group.update()
        player_sprite.update()
        fire_group.update()

        screen.fill(pygame.Color('black'))

        fire_group.draw(screen)
        all_sprites.draw(screen)
        volcano_group.draw(screen)
        player_sprite.draw(screen)
        plane_group.draw(screen)

        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()


def menu():
    running = True
    fon = pygame.transform.scale(load_image('menu_back.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    w = 150
    h = 50
    play = Button(button_group, (50, 50, w, h), screen, 'ИГРАТЬ', start_main)
    rules = Button(button_group, (50, 150, w, h), screen, 'ПРАВИЛА', start_screen)
    table = Button(button_group, (50, 250, w, h), screen, 'ЛИДЕРЫ', None)
    out = Button(button_group, (50, 350, w, h), screen, 'ВЫХОД', terminate)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                pos = event.pos
                if play.coords[0] <= pos[0] <= play.coords[0] + w and play.coords[1] <= pos[1] <= \
                        play.coords[1] + h:
                    play.mouse_down = True
                else:
                    play.mouse_down = False
                if rules.coords[0] <= pos[0] <= rules.coords[0] + w and rules.coords[1] <= pos[1] <= \
                        rules.coords[
                            1] + h:
                    rules.mouse_down = True
                else:
                    rules.mouse_down = False
                if table.coords[0] <= pos[0] <= table.coords[0] + w and table.coords[1] <= pos[1] <= \
                        table.coords[
                            1] + h:
                    table.mouse_down = True
                else:
                    table.mouse_down = False
                if out.coords[0] <= pos[0] <= out.coords[0] + w and out.coords[1] <= pos[1] <= \
                        out.coords[1] + h:
                    out.mouse_down = True
                else:
                    out.mouse_down = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if play.coords[0] <= pos[0] <= play.coords[0] + w and play.coords[1] <= pos[1] <= \
                        play.coords[1] + h:
                    return GAME
                if rules.coords[0] <= pos[0] <= rules.coords[0] + w and rules.coords[1] <= pos[1] <= \
                        rules.coords[
                            1] + h:
                    return GREETING
                if out.coords[0] <= pos[0] <= out.coords[0] + w and out.coords[1] <= pos[1] <= \
                        out.coords[1] + h:
                    return EXIT

        clock.tick(FPS)
        button_group.update()
        pygame.display.flip()
    pygame.quit()


tile_images = {'volcano': load_image('volcano.png'), 'empty': load_image('earth.jpg'),
               'plane': load_image('plane.png', -1)}

all_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
volcano_group = pygame.sprite.Group()
button_group = pygame.sprite.Group()
plane_group = pygame.sprite.Group()
dino_group = pygame.sprite.Group()
fire_group = pygame.sprite.Group()

GREETING = 0
MENU = 1
GAME = 2
RESULTS = 3
EXIT = 4

todo = {GREETING: start_screen,
        MENU: menu,
        GAME: start_main,
        RESULTS: None,
        EXIT: terminate}

player, x, y, plane = generate_level(load_level('first.txt'))
state = GREETING
while True:
    state = todo[state]()
