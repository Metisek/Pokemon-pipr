import pygame
from pygame_objects import Button, COLORS, FONTS
from database import PyGameObjectsDatabase, TextDatabase

pygame.init()

# Create game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FPS = 30


class Screen:
    def __init__(self):
        self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._clock = pygame.time.Clock()
        pygame.display.set_caption("Pokemon - Mateusz Bojarski")

    def get_clock(self):
        return self._clock

    def _get_screen(self):
        return self._screen

    def update_display(self):
        pygame.display.update()

    def draw_objects(self, objects_dict: dict[str]) -> None:
        objects = objects_dict.values()
        for object in objects:
            if isinstance(object, Button):
                self._draw_button(object)
            else:
                pass

    def draw_clear_text(
            self, pos, text,
            font='MEDIUM_FONT', color='INPURE_WHITE', align='center'
            ):
        screen = self._get_screen()
        anchor = pygame.Rect(pos, (1, 1))
        text_surf = FONTS.get(font).render(
            text, True, COLORS.get(color)
        )
        if align == 'center':
            text_rect = text_surf.get_rect(
                center=anchor.center
                )
        elif align == 'left':
            text_rect = text_surf.get_rect(
                midleft=anchor.midleft)
        elif align == 'right':
            text_rect = text_surf.get_rect(
                midright=anchor.midright)
        screen.blit(text_surf, text_rect)

    def draw_multiline_text(
            self, pos, text_lines, fsize=40,
            font='MEDIUM_FONT', color='INPURE_WHITE', align='center'
            ):
        for idx, line in enumerate(text_lines):
            pos_x = pos[0]
            pos_y = pos[1] + idx * fsize
            self.draw_clear_text((pos_x, pos_y), line, font, color, align)

    def draw_bg(self):
        self._get_screen().fill(COLORS.get('BG_COLOR'))

    def _draw_button(self, button_object: Button) -> None:
        screen = self._get_screen()
        draw_val = button_object.get_draw_values()
        pygame.draw.rect(screen, draw_val[0],
                         draw_val[1], border_radius=12)
        pygame.draw.rect(screen, draw_val[2],
                         pygame.Rect(draw_val[3]), 3, border_radius=12)
        screen.blit(draw_val[4], draw_val[5])


class PokemonGame:
    def __init__(self):
        self._game_state = 'main_menu'
        self._menu_state = 'main_menu'
        self._player_count = None
        self._objects_database = PyGameObjectsDatabase()
        pygame.display.set_caption("Pokemon - Mateusz Bojarski")

    def raised_event(self, object_key):
        active_objects = self.get_active_objects()
        try:
            object = active_objects.get(object_key)
            return object.raise_event()
        except BaseException:
            return False

    def get_active_objects(self):
        return self._objects_database.get_active_objects(
            self.get_game_state(), self.get_menu_state()
        )

    def get_game_state(self):
        return self._game_state

    def get_menu_state(self):
        return self._menu_state

    def set_game_state(self, game_state):
        self._game_state = game_state

    def set_menu_state(self, menu_state):
        self._menu_state = menu_state

    def set_player_count(self, players: int) -> None:
        self._player_count = players


def main():
    run = True
    screen = Screen()
    game = PokemonGame()
    text_database = TextDatabase()
    while run:
        screen.get_clock().tick(FPS)

        # Game widget events
        g_state = game.get_game_state()
        m_state = game.get_menu_state()

        if g_state == 'main_menu':
            if m_state == 'main_menu':
                if game.raised_event('play_button'):
                    print('MAMY TO!')
                    game.set_menu_state('players_select')
                elif game.raised_event('credits_button'):
                    print('CREDITS')
                    game.set_menu_state('credits_menu')
                elif game.raised_event('quit_button'):
                    run = False

            elif m_state == 'credits_menu':
                if game.raised_event('back_button'):
                    game.set_menu_state('main_menu')

            elif m_state == 'players_select':
                if game.raised_event('1_player_button'):
                    game.set_game_state('game_init')
                    game.set_menu_state('player_one_init')
                    game.set_player_count(1)
                elif game.raised_event('2_player_button'):
                    game.set_game_state('game_init')
                    game.set_menu_state('player_one_init')
                    game.set_player_count(2)
                elif game.raised_event('back_button'):
                    game.set_menu_state('main_menu')

        # Game draw static objects

        objects = game.get_active_objects()
        screen.draw_bg()

        if g_state == 'main_menu':
            if m_state == 'main_menu':
                screen.draw_clear_text((399, 150), "Pokemon game",
                                       font="BIG_FONT")
                pass
            elif m_state == 'credits_menu':
                text_credits = text_database.get_text('credits')
                screen.draw_multiline_text(
                    (399, 200), text_credits
                    )
            elif m_state == 'players_select':
                pass
        elif g_state == 'game_init':
            if m_state == 'player_one_init':
                pass
            elif m_state == 'player_two_init':
                pass
            elif m_state == 'start_game':
                pass

        screen.draw_objects(objects)
        screen.update_display()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()


if __name__ == '__main__':
    main()
