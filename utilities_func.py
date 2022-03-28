import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


def render_text(screen, myfont, screen_width, screen_height, tempo_scritte, text):
    screen.fill(WHITE)
    if type(text) != list:
        text = [text]
    for i in range(len(text)):
        label = myfont.render(text[i], 1, (0, 0, 0))
        text_rect = label.get_rect(center=(screen_width / 2, screen_height / 2 - 40 + i*40))
        screen.blit(label, text_rect)
    pygame.display.flip()
    pygame.time.wait(tempo_scritte)