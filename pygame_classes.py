import pygame

pygame.init()

COLORS = {
    'BG_COLOR': (25, 25, 45),
    'INPURE_WHITE': (239, 221, 249),
    'LIGHT_GRAY': (200, 208, 218),
    'WHITE': (255, 255, 255),
    'BLUEISH_BLACK': (13, 15, 25),
    'DARK_BLUE': (35, 28, 79)
}

gui_font = pygame.font.SysFont("arialblack", 20)


class Button:
    def __init__(self, text: str, size: tuple[float, float],
                 pos: tuple[float, float]) -> None:

        # Core attributes
        self._is_pressed = False
        self.original_y_pos = pos[1]
        self.elevation = 2
        self.dynamic_elecation = 2
        self._raise_event = False

        # Draw: top rectangle
        self.top_rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.top_color = COLORS.get('LIGHT_GRAY')

        # Draw: bottom_rectangle
        self.bottom_rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.bottom_color = COLORS.get('BLUEISH_BLACK')

        # Text:
        self.text = text
        self.text_surf = gui_font.render(
            text, True, COLORS.get('INPURE_WHITE')
        )
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def set_text(self, new_text):
        self.text = new_text
        self.text_surf = gui_font.render(
            new_text, True, COLORS.get('INPURE_WHITE')
        )
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def get_draw_values(self):
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation
        self.check_click()
        return (self.bottom_color, self.bottom_rect,
                self.top_color, self.top_rect,
                self.text_surf, self.text_rect
                )

    def check_click(self):
        self._raise_event = False
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = COLORS.get('INPURE_WHITE')
            self.bottom_color = COLORS.get('DARK_BLUE')
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self._is_pressed = True
                self.set_text(f"{self.text}")
            else:
                self.dynamic_elecation = self.elevation
                if self._is_pressed is True:
                    self._raise_event = True
                    self._is_pressed = False
                    self.set_text(self.text)
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = COLORS.get('LIGHT_GRAY')
            self.bottom_color = COLORS.get('BLUEISH_BLACK')
