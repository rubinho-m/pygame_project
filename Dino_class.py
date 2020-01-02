import pygame
import os
import time


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


tile_width = tile_height = 70
tile_images = {'volcano': load_image('volcano.png', -1), 'empty': load_image('earth.jpg'),
               'plane': load_image('plane.png', -1)}


class Dino(pygame.sprite.Sprite):
    def __init__(self, x, y, v, *args):
        super().__init__(args)
        self.frames = []
        a, b = v
        if a > 0:
            self.cut_sheet(pygame.transform.flip(load_image("1dragon_sheet8x2.png"), True, False), 8,
                           2)
        else:
            self.cut_sheet(load_image("1dragon_sheet8x2.png"), 8, 2)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x * 70, y * 60)
        self.x, self.y = x * 70, y * 60

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
