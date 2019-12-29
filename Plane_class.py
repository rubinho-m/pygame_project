import pygame
import os


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


tile_width = 70
tile_height = 60
width = 800
height = 600

tile_images = {'volcano': load_image('volcano.png', -1), 'empty': load_image('earth.jpg'), 'plane': load_image('plane.png', -1)}

class Plane(pygame.sprite.Sprite):
    image = load_image('plane.png', -1)
    def __init__(self, group):
        super().__init__(group)
        self.image = Plane.image
        self.rect = self.image.get_rect()
        self.rect.x = width - self.rect.w - 20
        self.rect.y = height - self.rect.h
