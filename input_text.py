import pygame

def input_text():
    FPS = 30
    WIDTH = 840
    HEIGHT = 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True

    font_s = 40
    font_head = pygame.font.Font(None, font_s)

    line = font_head.render('ВВЕДИТЕ СВОЁ ИМЯ:', 1, pygame.Color('black'))

    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    text = ''
    font_size = 40
    font = pygame.font.Font(None, font_size)
    string_rendered = font.render(text, 1, pygame.Color('black'))
    x = WIDTH // 2 - 50
    y = HEIGHT // 2 - 100
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
                if event.key == pygame.K_RETURN:
                    running = False
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                    string_rendered = font.render(text, 1, pygame.Color('black'))
                if event.key == pygame.K_SPACE:
                    text += ' '
                    string_rendered = font.render(text, 1, pygame.Color('black'))
        screen.fill(pygame.Color("yellow"))
        screen.blit(string_rendered, (x, y))

        screen.blit(line, (WIDTH // 2 - 150, 50))

        pygame.display.flip()
        clock.tick(FPS)

    return text
