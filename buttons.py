import os
import pygame
import math


class Button(pygame.sprite.Sprite):

    def __init__(self, group, coords, sc, text, func, left=False):
        super().__init__(group)
        self.scale = 140
        self.coords = coords
        self.sc = sc
        self.text = text
        self.func = func
        self.mouse_down = False
        self.color = (151, 176, 223)
        self.down_color = (223, 105, 148)
        self.font_size = 30
        self.font = pygame.font.Font('18337.otf', self.font_size)
        self.string_rendered = self.font.render(self.text, 1, pygame.Color('black'))
        self.left = left

    def update(self):
        if not self.mouse_down:
            pygame.draw.rect(self.sc, self.color, self.coords)
        else:
            pygame.draw.rect(self.sc, self.down_color, self.coords)
        if self.text == 'ПРАВИЛА' or self.text == 'ЛИДЕРЫ':
            x = self.coords[0] + self.coords[2] // 2 - (math.floor((len(self.text) // 2)) * self.font_size) // 2
        elif self.text == 'ИГРАТЬ':
            x = self.coords[0] + self.coords[2] // 2 - self.coords[2] // 4
        else:
            x = self.coords[0] + self.coords[2] // 2 - self.coords[2] // 3.5
        if self.left:
            x = self.coords[0] * 1.2
        if 'MUSIC' in self.text:
            x = self.coords[0] * 1.03
        if 'NEW GAME' in self.text:
            x = self.coords[0] * 1.33
        if 'PLAY' in self.text or 'EXIT' in self.text:
            x = self.coords[0] * 1.95
        if 'RULES' in self.text:
            x = self.coords[0] * 1.85
        if 'LEADERS' in self.text:
            x = self.coords[0] * 1.55
        y = self.coords[1] + self.coords[3] // 2 - self.font_size // 2
        self.string_rendered = self.font.render(self.text, 1, pygame.Color('black'))
        self.sc.blit(self.string_rendered, (x, y))
