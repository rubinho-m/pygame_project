import os
import pygame

pygame.init()
FPS = 30
WIDTH = 840
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
text = ''
font_size = 30
font = pygame.font.Font(None, font_size)
string_rendered = font.render(text, 1, pygame.Color('black'))
x = WIDTH // 2
y = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            try:
                text += ALPHABET[event.key - 97].upper()
                string_rendered = font.render(text, 1, pygame.Color('black'))
            except Exception:
                pass
            if event.key == pygame.K_BACKSPACE:
                text = text[:-1]
                string_rendered = font.render(text, 1, pygame.Color('black'))
            if event.key == pygame.K_SPACE:
                text += ' '
                string_rendered = font.render(text, 1, pygame.Color('black'))
    screen.fill(pygame.Color("yellow"))
    screen.blit(string_rendered, (x, y))
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
