import pygame
import os
import sys
import random
from Board_class import Board
from Volcano_class import Volcano
from Earth_class import Earth
from anim_sprite import Player
from buttons import Button
from Plane_class import Plane
from Dino_class import Dino
from FireBall_class import FireBall
import sqlite3
from input_text import input_text

pygame.init()
size = (width, height) = 840, 600
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('black'))
clock = pygame.time.Clock()

FPS = 25
lang = 'ru'
FONT = '16908.otf'
DB_LEADERS = 'leaders.db'
k = 0
start_k = 0
first_time = 0
menu_time = 0
music_flag = True
stop_game = False

levels = ['first.txt', 'second.txt', 'third.txt', 'fourth.txt']

# def load_db(filename):
#
#
#     return cur, bd[:10]

levels = ['first.txt', 'second.txt', 'third.txt', 'fourth.txt', 'fifth.txt']

die = False


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
            elif level[y][x] == '.':
                Earth('empty', x, y, empty_group)
    # второй цикл добавляет динозавров на поле с определением движения пламени
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'D':
                vect = count_space(x, y)
                Dino(x, y, vect, dino_group, all_sprites)
                FireBall(x * 70, y * 60, vect, False, fire_group, all_sprites)
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
    global start_k, lang, menu_time, stop_game
    if lang == 'ru':
        intro_text = ["Эра динозавров", "",
                      "Вы попали в джунгли Юрского периода,",
                      "и Вам предстоит добраться до своего",
                      "реактивного самолёта, минуя динозавров",
                      "и избегая ударов метеоритов.",
                      'Вы можете прятаться в стоге сена,',
                      'но при попадании в него огненного шара',
                      'игрок будет перемещён в стартовую точку.',
                      'Метеориты будут пролетать с периодичностью в 7с.',
                      'Будьте осторожны и внимательны:',
                      'дорога таит в себе много опасностей... Удачи!',
                      'Нажмите любую кнопку, чтобы продолжить.']
    elif lang == 'eng':
        intro_text = ["The Age of Dinosaurs", "",
                      "You are trapped in the Jurassic jungle,",
                      "and you have to get to your jet plane.",
                      "Avoid dinosaurs and meteorite falling.",
                      'You can hide in a haystack,',
                      'but when a fireball hits it',
                      'the player will be moved to the starting point.',
                      'Meteorites will fly in 7 seconds.',
                      "Be careful: the road is very",
                      "dangerous... Good luck!",
                      'Push any button to continue.']

    fon = pygame.transform.scale(load_image('start_dino.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    line = intro_text[0]
    string_rendered = font.render(line, 6, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    text_coord = 20
    intro_rect.top = text_coord
    intro_rect.x = 310
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)
    text_coord = 20
    start_time = pygame.time.get_ticks()
    for line in intro_text[1:]:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 200
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    if start_k == 0:
        pygame.mixer.music.load(os.path.join('sounds', 'bg_music.wav'))
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(loops=-1)
    start_k += 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if stop_game:
                    menu_time += last_time - start_time
                return MENU
        pygame.display.flip()
        clock.tick(FPS)
        last_time = pygame.time.get_ticks()


def start_main(new_game=False, level=None):
    global k, first_time, new_time, menu_time, lang, stop_game, die, player, pos_x, pos_y
    if die:
        die = False
        menu_time = 0
        player.rect.x = pos_x * 70
        player.rect.y = pos_y * 60

    if new_game:
        menu_time = 0
        all_sprites.empty()
        player_sprite.empty()
        volcano_group.empty()
        plane_group.empty()
        dino_group.empty()
        fire_group.empty()
        meteorites_group.empty()

        if level is None:

            player, pos_x, pos_y, plane = generate_level(load_level(random.choice(levels)))
        elif level == 1:
            player, pos_x, pos_y, plane = generate_level(load_level('first.txt'))
        elif level == 2:
            player, pos_x, pos_y, plane = generate_level(load_level('second.txt'))
        elif level == 3:
            player, pos_x, pos_y, plane = generate_level(load_level('third.txt'))
        elif level == 4:
            player, pos_x, pos_y, plane = generate_level(load_level('fourth.txt'))
        elif level == 5:
            player, pos_x, pos_y, plane = generate_level(load_level('fifth.txt'))

        die = False
        player.rect.x = pos_x * 70
        player.rect.y = pos_y * 60

    player.rect.w = player.player_scale
    player.rect.h = player.player_scale
    step = 5
    running = True
    w = 70
    h = 60
    button_group_game = pygame.sprite.Group()
    if lang == 'ru':
        cancel = Button(button_group_game, (0, 0, w, h), screen, 'МЕНЮ', menu, True)
    elif lang == 'eng':
        cancel = Button(button_group_game, (0, 0, w, h), screen, 'MENU', menu, True)
    METEORITEEVENT = 30
    pygame.time.set_timer(METEORITEEVENT, 6500)
    if new_game or k == 0:
        first_time = pygame.time.get_ticks()
    k += 1
    alarm_sound = pygame.mixer.Sound(os.path.join('sounds', 'alarm.wav'))
    scream_sound = pygame.mixer.Sound(os.path.join('sounds', 'scream.wav'))
    while running:
        for event in pygame.event.get():
            if event.type == METEORITEEVENT:
                FireBall(random.randint(0, width), -height, (0, 1), True, meteorites_group,
                         all_sprites)
                alarm_sound.play()
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                pos = event.pos
                if cancel.coords[0] <= pos[0] <= cancel.coords[0] + w and cancel.coords[1] <= pos[
                    1] <= \
                        cancel.coords[1] + h:
                    cancel.mouse_down = True
                else:
                    cancel.mouse_down = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if cancel.coords[0] <= pos[0] <= cancel.coords[0] + w and cancel.coords[1] <= pos[
                    1] <= \
                        cancel.coords[1] + h:
                    stop_game = True
                    return MENU
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.rotate = False
            player.rect.x += step
            player_sprite.update()
            collide = pygame.sprite.groupcollide(player_sprite, volcano_group, False, False)
            if len(collide) != 0:
                player.rect.x -= step
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.rotate = True
            player.rect.x -= step
            player_sprite.update()
            player.image = pygame.transform.flip(player.image, True, False)
            collide = pygame.sprite.groupcollide(player_sprite, volcano_group, False, False)
            if len(collide) != 0:
                player.rect.x += step

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.rect.y -= step
            player_sprite.update()
            collide = pygame.sprite.groupcollide(player_sprite, volcano_group, False, False)
            if len(collide) != 0:
                player.rect.y += step
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.rect.y += step
            player_sprite.update()
            collide = pygame.sprite.groupcollide(player_sprite, volcano_group, False, False)
            if len(collide) != 0:
                player.rect.y -= step
        if not keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_LEFT] and not \
                keys[
                    pygame.K_RIGHT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_d] and not \
                keys[
                    pygame.K_a] and not keys[
            pygame.K_w] and not keys[pygame.K_s]:
            player.state = False
        else:
            player.state = True

        for fire in fire_group:
            if pygame.sprite.spritecollideany(fire, volcano_group, False):
                fire.return_back()
        collide_plane = pygame.sprite.groupcollide(player_sprite, plane_group, False, False)
        collide_fire = pygame.sprite.groupcollide(player_sprite, fire_group, False, False)
        collide_dino = pygame.sprite.groupcollide(player_sprite, dino_group, False, False)
        collide_meteorite = pygame.sprite.groupcollide(player_sprite, meteorites_group, False, False)
        for meteorite in meteorites_group:
            if meteorite.rect.y >= 300:
                meteorites_group.remove(meteorite)
        if len(collide_plane) != 0:
            player.rect.x = pos_x * 70
            player.rect.y = pos_y * 60
            k = 0
            pygame.mixer.stop()

            con = sqlite3.connect(DB_LEADERS)
            cur = con.cursor()

            bd = cur.execute('SELECT * from players ORDER BY time').fetchall()

            cur.execute('DELETE from players')

            for name, t in bd:
                cur.execute(f"""INSERT INTO players(name, time) VALUES ({', '.join(
                    ["'" + str(x) + "'" for x in [name, t]])})""")

            bd = bd[:10]

            if len(bd) < 10 or int(time) < bd[-1][-1]:
                name = input_text()
                cur.execute(f"""INSERT INTO players(name, time) VALUES({', '.join(
                    ["'" + str(x) + "'" for x in [name, time]])})""")

            con.commit()
            con.close()

            return RESULTS
        if len(collide_fire) != 0:
            for fire in fire_group:
                fire.return_back()
            if not player.state:
                player.rect.x = pos_x * 70
                player.rect.y = pos_y * 60
                scream_sound.play()
            else:
                k = 0
                pygame.mixer.stop()
                scream_sound.play()
                return LOSE
        if len(collide_meteorite) != 0:
            for meteorite in meteorites_group:
                meteorites_group.remove(meteorite)
            if not player.state:
                player.rect.x = pos_x * 70
                player.rect.y = pos_y * 60
                scream_sound.play()
            else:
                k = 0
                pygame.mixer.stop()
                scream_sound.play()
                return LOSE
        if len(collide_dino) != 0:
            player.rect.x = pos_x * 70
            player.rect.y = pos_y * 60
            k = 0
            pygame.mixer.stop()
            scream_sound.play()
            return LOSE
        new_time = pygame.time.get_ticks()

        all_sprites.update()
        volcano_group.update()
        player_sprite.update()
        fire_group.update()

        screen.fill(pygame.Color('black'))

        fire_group.draw(screen)
        volcano_group.draw(screen)
        plane_group.draw(screen)
        meteorites_group.draw(screen)
        all_sprites.draw(screen)
        player_sprite.draw(screen)
        button_group_game.update()

        delta = (new_time - first_time) // 1000

        time = str(delta - menu_time // 1000)
        if int(time) < 0:
            time = '0'
        font_size = 100
        font = pygame.font.Font(FONT, font_size)
        string_rendered = font.render(time, 1, pygame.Color('black'))
        screen.blit(string_rendered, (width // 2, 0))

        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()


def menu():
    global menu_time, k, music_flag, stop_game, lang
    first_time = pygame.time.get_ticks()
    running = True
    fon = pygame.transform.scale(load_image('menu_back.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    w = 150
    h = 50
    x = 50
    font_size = 60
    font = pygame.font.Font(FONT, font_size)
    if lang == 'ru':
        new_play = Button(button_group, (x, 50, w, h), screen, 'НОВАЯ ИГРА', start_main, True)
        play = Button(button_group, (x, 150, w, h), screen, 'ИГРАТЬ', start_main)
        rules = Button(button_group, (x, 250, w, h), screen, 'ПРАВИЛА', start_screen)
        table = Button(button_group, (x, 350, w, h), screen, 'ЛИДЕРЫ', finish)
        out = Button(button_group, (x, 540, w, h), screen, 'ВЫХОД', terminate)
        level_b = Button(button_group, (x, 450, w, h), screen, 'УРОВНИ', choose_level)
        language = Button(button_group, (width - w - 10, height - h - 10, w, h), screen, 'ENGLISH',
                          terminate)
        title = 'ЭРА ДИНОЗАВРОВ'
    elif lang == 'eng':
        new_play = Button(button_group, (x, 50, w, h), screen, 'NEW GAME', start_main, True)
        play = Button(button_group, (x, 150, w, h), screen, 'PLAY', start_main)
        rules = Button(button_group, (x, 250, w, h), screen, 'RULES', start_screen)
        table = Button(button_group, (x, 350, w, h), screen, 'LEADERS', finish)
        level_b = Button(button_group, (x, 450, w, h), screen, 'LEVELS', choose_level)
        out = Button(button_group, (x, 540, w, h), screen, 'EXIT', terminate)
        language = Button(button_group, (width - w - 10, height - h - 10, w, h), screen, 'RUSSIAN',
                          terminate)
        title = 'THE AGE OF DINOSAURS'
    string_rendered = font.render(title, True, pygame.Color('black'))
    music = Button(button_group, (width - w, 0, w, h), screen, 'MUSIC: ON', None, True)
    if not music_flag:
        music.text = 'MUSIC: OFF'
    button_group.update()
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
                if new_play.coords[0] <= pos[0] <= new_play.coords[0] + w and new_play.coords[1] <= \
                        pos[1] <= \
                        new_play.coords[1] + h:
                    new_play.mouse_down = True
                else:
                    new_play.mouse_down = False
                if music.coords[0] <= pos[0] <= music.coords[0] + w and music.coords[1] <= pos[1] <= \
                        music.coords[1] + h:
                    music.mouse_down = True
                else:
                    music.mouse_down = False
                if language.coords[0] <= pos[0] <= language.coords[0] + w and language.coords[1] <= \
                        pos[1] <= \
                        language.coords[1] + h:
                    language.mouse_down = True
                else:
                    language.mouse_down = False
                if level_b.coords[0] <= pos[0] <= level_b.coords[0] + w and level_b.coords[1] <= \
                        pos[1] <= \
                        level_b.coords[1] + h:
                    level_b.mouse_down = True
                else:
                    level_b.mouse_down = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if play.coords[0] <= pos[0] <= play.coords[0] + w and play.coords[1] <= pos[1] <= \
                        play.coords[1] + h:
                    if stop_game:
                        menu_time += (last_time - first_time)
                        stop_game = False
                    return GAME
                if new_play.coords[0] <= pos[0] <= new_play.coords[0] + w and new_play.coords[1] <= \
                        pos[1] <= \
                        new_play.coords[1] + h:
                    stop_game = False
                    return NEW_GAME
                if rules.coords[0] <= pos[0] <= rules.coords[0] + w and rules.coords[1] <= pos[1] <= \
                        rules.coords[
                            1] + h:
                    if stop_game:
                        menu_time += (last_time - first_time)
                    return GREETING
                if out.coords[0] <= pos[0] <= out.coords[0] + w and out.coords[1] <= pos[1] <= \
                        out.coords[1] + h:
                    return EXIT
                if table.coords[0] <= pos[0] <= table.coords[0] + w and table.coords[1] <= pos[1] <= \
                        table.coords[1] + h:
                    if stop_game:
                        menu_time += (last_time - first_time)
                    return RESULTS
                if music.coords[0] <= pos[0] <= music.coords[0] + w and music.coords[1] <= pos[1] <= \
                        music.coords[1] + h:
                    if music_flag:
                        music_flag = False
                        music.text = 'MUSIC: OFF'
                    else:
                        music_flag = True
                        music.text = 'MUSIC: ON'

                if level_b.coords[0] <= pos[0] <= level_b.coords[0] + w and level_b.coords[1] <= pos[
                    1] <= \
                        level_b.coords[1] + h:
                    if stop_game:
                        menu_time += (last_time - first_time)
                    return LEVELS
                if language.coords[0] <= pos[0] <= language.coords[0] + w and language.coords[1] <= \
                        pos[1] <= \
                        language.coords[1] + h:
                    if lang == 'ru':
                        lang = 'eng'
                    elif lang == 'eng':
                        lang = 'ru'
                    if lang == 'ru':
                        new_play = Button(button_group, (x, 50, w, h), screen, 'НОВАЯ ИГРА',
                                          start_main, True)
                        play = Button(button_group, (x, 150, w, h), screen, 'ИГРАТЬ', start_main)
                        rules = Button(button_group, (x, 250, w, h), screen, 'ПРАВИЛА', start_screen)
                        table = Button(button_group, (x, 350, w, h), screen, 'ЛИДЕРЫ', finish)
                        level_b = Button(button_group, (x, 450, w, h), screen, 'УРОВНИ',
                                         choose_level)
                        out = Button(button_group, (x, 540, w, h), screen, 'ВЫХОД', terminate)
                        language = Button(button_group, (width - w - 10, height - h - 10, w, h),
                                          screen, 'ENGLISH',
                                          terminate)
                        title = 'ЭРА ДИНОЗАВРОВ'
                    elif lang == 'eng':
                        new_play = Button(button_group, (x, 50, w, h), screen, 'NEW GAME',
                                          start_main, True)
                        play = Button(button_group, (x, 150, w, h), screen, 'PLAY', start_main)
                        rules = Button(button_group, (x, 250, w, h), screen, 'RULES', start_screen)
                        table = Button(button_group, (x, 350, w, h), screen, 'LEADERS', finish)
                        level_b = Button(button_group, (x, 450, w, h), screen, 'LEVELS',
                                         choose_level)
                        out = Button(button_group, (x, 540, w, h), screen, 'EXIT', terminate)
                        language = Button(button_group, (width - w - 10, height - h - 10, w, h),
                                          screen, 'RUSSIAN',
                                          terminate)
                        title = 'THE AGE OF DINOSAURS'
                    string_rendered = font.render(title, True, pygame.Color('black'))
        last_time = pygame.time.get_ticks()
        if not music_flag:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(0.4)
        screen.fill(pygame.Color('black'))
        screen.blit(fon, (0, 0))
        screen.blit(string_rendered, (275, 0))

        clock.tick(FPS)
        button_group.update()
        pygame.display.flip()

    pygame.quit()


def finish():
    global lang, menu_time, stop_game
    running = True
    fon = pygame.transform.scale(load_image('table.jpg'), (width, height))
    button_group_table = pygame.sprite.Group()
    screen.blit(fon, (0, 0))
    w = 150
    h = 50
    if lang == 'ru':
        cancel = Button(button_group_table, (0, 0, w, h), screen, 'МЕНЮ', menu)
        text = 'Таблица рекордов'
        x, y = 265, 0
    elif lang == 'eng':
        cancel = Button(button_group_table, (0, 0, w, h), screen, 'MENU', menu)
        text = 'Table of records'
        x, y = 300, 0
    font_size = 60
    font = pygame.font.Font(None, font_size)
    string_rendered = font.render(text, 1, pygame.Color('black'))
    screen.blit(string_rendered, (x, y))
    start_time = pygame.time.get_ticks()

    con = sqlite3.connect(DB_LEADERS)
    cur = con.cursor()

    bd = cur.execute('SELECT * from players ORDER BY time').fetchall()[:10]

    font_size = 40
    font = pygame.font.Font(None, font_size)
    x, y = 100, 100

    for name, time in bd:
        name_r = font.render(name, 1, pygame.Color('black'))
        time_r = font.render(str(time), 1, pygame.Color('black'))

        screen.blit(name_r, (x, y))
        screen.blit(time_r, (x + 600, y))
        y += 40

    x, y = 90, 90
    for _ in range(10):
        pygame.draw.rect(screen, (0, 0, 0), (x, y, 600, 40), 1)
        pygame.draw.rect(screen, (0, 0, 0), (x + 600, y, 80, 40), 1)
        y += 40

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                pos = event.pos
                if cancel.coords[0] <= pos[0] <= cancel.coords[0] + w and cancel.coords[1] <= pos[
                    1] <= \
                        cancel.coords[1] + h:
                    cancel.mouse_down = True
                else:
                    cancel.mouse_down = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if cancel.coords[0] <= pos[0] <= cancel.coords[0] + w and cancel.coords[1] <= pos[
                    1] <= \
                        cancel.coords[1] + h:
                    if stop_game:
                        menu_time += last_time - start_time
                    return MENU
        clock.tick(FPS)
        button_group_table.update()
        pygame.display.flip()
        last_time = pygame.time.get_ticks()
    pygame.quit()


def lose():
    global lang, die
    running = True
    die = True
    fon = pygame.transform.scale(load_image('game_over.png'), (width, height))
    button_group_lose = pygame.sprite.Group()
    screen.blit(fon, (0, 0))
    w = 150
    h = 50
    if lang == 'ru':
        cancel = Button(button_group_lose, (0, 0, w, h), screen, 'МЕНЮ', menu)
        results = Button(button_group_lose, (width - w, 0, w, h), screen, 'ЛИДЕРЫ', finish)
    elif lang == 'eng':
        cancel = Button(button_group_lose, (0, 0, w, h), screen, 'MENU', menu)
        results = Button(button_group_lose, (width - w, 0, w, h), screen, 'RECORDS', finish)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                pos = event.pos
                if cancel.coords[0] <= pos[0] <= cancel.coords[0] + w and cancel.coords[1] <= pos[
                    1] <= \
                        cancel.coords[1] + h:
                    cancel.mouse_down = True
                else:
                    cancel.mouse_down = False
                if results.coords[0] <= pos[0] <= results.coords[0] + w and results.coords[1] <= pos[
                    1] <= \
                        results.coords[1] + h:
                    results.mouse_down = True
                else:
                    results.mouse_down = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if cancel.coords[0] <= pos[0] <= cancel.coords[0] + w and cancel.coords[1] <= pos[
                    1] <= \
                        cancel.coords[1] + h:
                    return MENU
                if results.coords[0] <= pos[0] <= results.coords[0] + w and results.coords[1] <= pos[
                    1] <= \
                        results.coords[1] + h:
                    return RESULTS
        clock.tick(FPS)
        button_group_lose.update()
        pygame.display.flip()
    pygame.quit()


def choose_level():
    global lang, menu_time, stop_game
    running = True
    fon = pygame.transform.scale(load_image('menu_back.jpg'), (width, height))
    button_group_choose = pygame.sprite.Group()
    screen.blit(fon, (0, 0))
    w = 150
    h = 50
    start_time = pygame.time.get_ticks()
    if lang == 'ru':
        cancel = Button(button_group_choose, (0, 0, w, h), screen, 'МЕНЮ', menu)
        first = Button(button_group_choose, (50, 80, w, h), screen, 'ПЕРВЫЙ', menu)
        second = Button(button_group_choose, (50, 180, w, h), screen, 'ВТОРОЙ', menu)
        third = Button(button_group_choose, (50, 280, w, h), screen, 'ТРЕТИЙ', menu)
        fourth = Button(button_group_choose, (50, 380, w, h), screen, 'ЧЕТВЕРТЫЙ', menu, True)
        fifth = Button(button_group_choose, (50, 480, w, h), screen, 'ПЯТЫЙ', menu)
    elif lang == 'eng':
        cancel = Button(button_group_choose, (0, 0, w, h), screen, 'MENU', menu)
        first = Button(button_group_choose, (50, 80, w, h), screen, 'FIRST', menu)
        second = Button(button_group_choose, (50, 180, w, h), screen, 'SECOND', menu)
        third = Button(button_group_choose, (50, 280, w, h), screen, 'THIRD', menu)
        fourth = Button(button_group_choose, (50, 380, w, h), screen, 'FOURTH', menu)
        fifth = Button(button_group_choose, (50, 480, w, h), screen, 'FIFTH', menu)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                pos = event.pos
                if cancel.coords[0] <= pos[0] <= cancel.coords[0] + w and cancel.coords[1] <= pos[
                    1] <= \
                        cancel.coords[1] + h:
                    cancel.mouse_down = True
                else:
                    cancel.mouse_down = False
                if first.coords[0] <= pos[0] <= first.coords[0] + w and first.coords[1] <= pos[1] <= \
                        first.coords[1] + h:
                    first.mouse_down = True
                else:
                    first.mouse_down = False
                if second.coords[0] <= pos[0] <= second.coords[0] + w and second.coords[1] <= pos[
                    1] <= \
                        second.coords[1] + h:
                    second.mouse_down = True
                else:
                    second.mouse_down = False
                if third.coords[0] <= pos[0] <= third.coords[0] + w and third.coords[1] <= pos[1] <= \
                        third.coords[1] + h:
                    third.mouse_down = True
                else:
                    third.mouse_down = False
                if fourth.coords[0] <= pos[0] <= fourth.coords[0] + w and fourth.coords[1] <= pos[
                    1] <= \
                        fourth.coords[1] + h:
                    fourth.mouse_down = True
                else:
                    fourth.mouse_down = False
                if fifth.coords[0] <= pos[0] <= fifth.coords[0] + w and fifth.coords[1] <= pos[1] <= \
                        fifth.coords[1] + h:
                    fifth.mouse_down = True
                else:
                    fifth.mouse_down = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if cancel.coords[0] <= pos[0] <= cancel.coords[0] + w and cancel.coords[1] <= pos[
                    1] <= \
                        cancel.coords[1] + h:
                    if stop_game:
                        menu_time += last_time - start_time
                    return MENU
                if first.coords[0] <= pos[0] <= first.coords[0] + w and first.coords[1] <= pos[1] <= \
                        first.coords[1] + h:
                    return FIRST
                if second.coords[0] <= pos[0] <= second.coords[0] + w and second.coords[1] <= pos[
                    1] <= \
                        second.coords[1] + h:
                    return SECOND
                if third.coords[0] <= pos[0] <= third.coords[0] + w and third.coords[1] <= pos[1] <= \
                        third.coords[1] + h:
                    return THIRD
                if fourth.coords[0] <= pos[0] <= fourth.coords[0] + w and fourth.coords[1] <= pos[
                    1] <= \
                        fourth.coords[1] + h:
                    return FOURTH
                if fifth.coords[0] <= pos[0] <= fifth.coords[0] + w and fifth.coords[1] <= pos[1] <= \
                        fifth.coords[1] + h:
                    return FIFTH
        clock.tick(FPS)
        button_group_choose.update()
        pygame.display.flip()
        last_time = pygame.time.get_ticks()
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
empty_group = pygame.sprite.Group()
meteorites_group = pygame.sprite.Group()

tile_width = 70
tile_height = 60

GREETING = 0
MENU = 1
GAME = 2
RESULTS = 3
EXIT = 4
LOSE = 5
NEW_GAME = 6
LEVELS = 7
FIRST = 8
SECOND = 9
THIRD = 10
FOURTH = 11
FIFTH = 12

todo = {GREETING: start_screen,
        MENU: menu,
        GAME: start_main,
        RESULTS: finish,
        EXIT: terminate,
        LOSE: lose,
        NEW_GAME: lambda: start_main(True),
        LEVELS: choose_level,
        FIRST: lambda: start_main(True, 1),
        SECOND: lambda: start_main(True, 2),
        THIRD: lambda: start_main(True, 3),
        FOURTH: lambda: start_main(True, 4),
        FIFTH: lambda: start_main(True, 5)}

player, pos_x, pos_y, plane = generate_level(load_level(random.choice(levels)))
state = GREETING
while True:
    state = todo[state]()
