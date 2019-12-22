import os
import pygame

pygame.init()

FPS = 30
WIDTH = 1080
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()


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


class AnimatedSprite(pygame.sprite.Sprite):

    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.scale = 140
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
                self.image = pygame.transform.flip(player.image, True, False)
            self.image = self.idle


player = AnimatedSprite(load_image("player_anim.png", -1), 7, 4, 0, 0)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player.rotate = False
        player.rect.x += 10
        all_sprites.update()
    if keys[pygame.K_LEFT]:
        player.rotate = True
        player.rect.x -= 10
        all_sprites.update()
        player.image = pygame.transform.flip(player.image, True, False)
    if keys[pygame.K_UP]:
        player.rect.y -= 10
        all_sprites.update()
    if keys[pygame.K_DOWN]:
        player.rect.y += 10
        all_sprites.update()
    if not keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
        player.state = False
    else:
        player.state = True
    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
