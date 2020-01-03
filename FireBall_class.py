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


class FireBall(pygame.sprite.Sprite):
    def __init__(self, x, y, vect, ismeteor, *args):
        super().__init__(args)
        self.frames = []
        self.cut_sheet(load_image("fire.png"), 8, 4)
        self.cur_frame = 0
        self.flag = ismeteor
        self.image = self.frames[self.cur_frame]
        if self.flag:
            self.image = pygame.transform.scale(self.image, (70, 70))

        self.vector = vect

        self.start_x, self.start_y = 0, 0

        a, b = self.vector
        if a < 0:
            self.start_x = x - 10
        elif a > 0:
            self.start_x = x + 40
        elif a == 0:
            self.start_x = x + 20
        if b < 0:
            self.start_y = y - 10
        elif b > 0:
            self.start_y = y + 40
        else:
            self.start_y = y + 10

        self.rect = self.rect.move(self.start_x, self.start_y)
        self.rect.x, self.rect.y = self.start_x, self.start_y

        self.appear = True

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
        if self.flag:
            self.image = pygame.transform.scale(self.image, (70, 70))

        if self.appear and self.cur_frame == 11:
            self.rect.x = self.start_x
            self.rect.y = self.start_y
        else:
            x, y = self.vector
            if x < 0:
                self.move(self.rect.x - 3, self.rect.y)
            elif x > 0:
                self.move(self.rect.x + 3, self.rect.y)
            elif y < 0:
                self.move(self.rect.x, self.rect.y - 3)
            else:
                if not self.flag:
                    self.move(self.rect.x, self.rect.y + 3)
                else:
                    self.move(self.rect.x, self.rect.y + 30)

        if self.appear:
            self.appear = False

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def return_back(self):
        self.rect = self.rect.move(self.start_x, self.start_y)
        self.rect.x, self.rect.y = self.start_x, self.start_y
        self.appear = True


if __name__ == '__main__':
    volcano_group = pygame.sprite.Group()
