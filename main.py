import pygame
from pygame_classes import Button, COLORS

pygame.init()

# Create game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FPS = 30

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")
clock = pygame.time.Clock()

buttons = []

button1 = Button('Warszawa', (200, 40), (100, 200))

buttons.append(button1)


def draw_button():
    for b in buttons:
        draw_val = b.get_draw_values()
        pygame.draw.rect(screen, draw_val[0],
                         draw_val[1], border_radius=12)
        pygame.draw.rect(screen, draw_val[2],
                         pygame.Rect(draw_val[3]), 3, border_radius=12)
        screen.blit(draw_val[4], draw_val[5])


def draw_display():
    screen.fill(COLORS.get('BG_COLOR'))
    draw_button()
    pygame.display.update()

# game variables

# game_paused = False
# menu_state = "main"


def main():
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_display()
    pygame.quit()


if __name__ == '__main__':
    main()
