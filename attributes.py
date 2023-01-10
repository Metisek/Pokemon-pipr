import pygame
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FPS = 30

FRAME_PATH = os.path.join('assets', 'pokemon_frame.png')
FRAME_IMAGE = pygame.image.load(FRAME_PATH)
DATABASE_PATH = 'pokemon.json'

COLORS = {
    'BG_COLOR': (25, 25, 45),
    'INPURE_WHITE': (239, 221, 249),
    'WHITE': (255, 255, 255),
    'LIGHT_GRAY': (200, 208, 218),
    'DARK_GRAY': (86, 86, 90),
    'DARK_BLUE': (35, 28, 79),
    'BLUEISH_BLACK': (13, 15, 25),
    'INPURE_BLACK': (8, 8, 14),
}

FONTS = {
    'GUI_FONT': pygame.font.SysFont("arialblack", 25),
    'BIG_FONT': pygame.font.SysFont("arial", 50),
    'MEDIUM_FONT': pygame.font.SysFont("calibri", 34),
    'SMALL_FONT': pygame.font.SysFont("calibri", 20),
    'SMALLER_FONT': pygame.font.SysFont("calibri", 12)
}
