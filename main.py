import pygame
from pygame_objects import (
    Button,
    PokemonList,
    PokemonListElem,
    PokemonBalls,
    PokemonFrame,
    SpecialList,
    GamePokemonList
)
from attributes import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    FPS,
    FONTS,
    COLORS
)
from random import randint, choice

from classes import (
    RedundantKeyError,
    PokemonDataDoesNotExistError
)

from tk_objects import TkPokemonSelectWindow
from database import PyGameObjectsDatabase, TextDatabase
from classes import BasePokemon, GamePokemon


pygame.init()


class Screen:
    """PyGame screen window class with drawing functions embedded
    """
    def __init__(self) -> None:
        """Initialises main screen with basic parameters set in attributes
        """
        self._screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), flags=0)
        self._clock = pygame.time.Clock()
        pygame.display.set_caption("Pokemon - Mateusz Bojarski")

    def get_clock(self) -> pygame.time.Clock:
        """Gets private value of screen's clock (FPS) and returns it

        Returns:
            pygame.time.Clock: Active clock object
        """
        return self._clock

    def _get_screen(self) -> pygame.display:
        """Gets private value of screen display object and returns it

        Returns:
            pygame.display: Acrive display
        """
        return self._screen

    def update_display(self):
        """Updates current pygame display
        """
        pygame.display.update()

    def draw_objects(self, objects_dict: dict[str]) -> None:
        objects = objects_dict.values()
        for object in objects:
            if isinstance(object, Button):
                self._draw_button(object)
            elif isinstance(object, GamePokemonList):
                self._draw_game_pokemon_list(object)
            elif isinstance(object, PokemonList):
                self._draw_list(object)
            elif isinstance(object, PokemonBalls):
                pass
            elif isinstance(object, PokemonFrame):
                self._draw_game_frame(object)
            elif isinstance(object, SpecialList):
                self._draw_special_list(object)

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

    def _draw_game_pokemon_list(self, list_object: GamePokemonList) -> None:
        if list_object.get_is_visible():
            self._draw_list(list_object)
        else:
            for elem in list_object.get_elem_list():
                elem._raise_event = False

    def _draw_special_list(self, list_object: SpecialList) -> None:
        draw_val = list_object.get_draw_values()
        if list_object.get_is_visible():
            screen = self._get_screen()
            main_frame = draw_val[0]
            pokemons_frame = draw_val[1]
            pygame.draw.rect(screen, main_frame[0],
                             main_frame[1], border_radius=12)
            pygame.draw.rect(screen, main_frame[2],
                             pygame.Rect(main_frame[3]), 3, border_radius=12)
            for elem in pokemons_frame:
                pygame.draw.rect(screen, elem[0][0],
                                 elem[0][1], border_radius=12)
                pygame.draw.rect(screen, elem[0][2],
                                 pygame.Rect(elem[0][3]),
                                 3, border_radius=12)
                screen.blit(elem[1][0], elem[1][1])

    def _draw_list(self, list_object: PokemonList) -> None:
        screen = self._get_screen()
        draw_val = list_object.get_draw_values()
        main_frame = draw_val[0]
        pokemons_frame = draw_val[1]
        pygame.draw.rect(screen, main_frame[0],
                         main_frame[1], border_radius=12)
        pygame.draw.rect(screen, main_frame[2],
                         pygame.Rect(main_frame[3]), 3, border_radius=12)
        for elem in pokemons_frame:
            pygame.draw.rect(screen, elem[0][0],
                             elem[0][1], border_radius=12)
            pygame.draw.rect(screen, elem[0][2],
                             pygame.Rect(elem[0][3]),
                             3, border_radius=12)
            for texts in elem[1]:
                screen.blit(texts[0], texts[1])

    def _draw_game_frame(self, frame_object: PokemonFrame):
        screen = self._get_screen()
        draw_val = frame_object.get_draw_values()
        image = draw_val[0]
        texts = draw_val[1]
        screen.blit(image[0], image[1])
        for text in texts:
            screen.blit(text[0], text[1])

    def _draw_button(self, button_object: Button) -> None:
        screen = self._get_screen()
        draw_val = button_object.get_draw_values()
        pygame.draw.rect(screen, draw_val[0],
                         draw_val[1], border_radius=12)
        pygame.draw.rect(screen, draw_val[2],
                         pygame.Rect(draw_val[3]), 3, border_radius=12)
        screen.blit(draw_val[4], draw_val[5])

    def draw_balls(self, object: PokemonBalls, count: int) -> None:
        screen = self._get_screen()
        draw_vals = object.get_draw_values(count)
        for elem in draw_vals:
            screen.blit(elem[0], elem[1])


class PokemonGame:
    def __init__(self):
        self._game_state = 'main_menu'
        self._menu_state = 'main_menu'
        self._player_count = None
        self._player_one_pokemons = []
        self._player_two_pokemons = []
        self._player_one_pokemon_number = 1
        self._player_two_pokemon_number = 1
        self._player_one_active_pokemon = None
        self._player_two_active_pokemon = None
        self._selected_pokemon = None
        self._selected_frame = None
        self._objects_database = PyGameObjectsDatabase()
        self._player_turn = None
        self._winner = None

    def game_init_handle(self, object_type: str | None, player: int) -> None:
        pokemon_number = self.get_given_player_pokemon_number(player)
        pokemon_list = self.get_given_player_poke_list(player)
        if object_type == 'remove_pokemon_button':
            self.set_selected_pokemon(None)
            self.set_selected_frame(None)
            self.get_object(
                'remove_pokemon_button').set_object_style('inactive')
        elif object_type == 'add_pokeballs_button':
            self._set_given_player_pokemon_number(pokemon_number + 1, player)
            pokemon_number = self.get_given_player_pokemon_number(player)
        elif object_type == 'remove_pokeballs_button':
            self._set_given_player_pokemon_number(pokemon_number - 1, player)
            pokemon_number = self.get_given_player_pokemon_number(player)

        self.get_object('continue_button').set_object_style('normal')
        self.get_object('add_pokemon_button').set_object_style('normal')
        self.get_object('add_pokeballs_button').set_object_style('normal')
        self.get_object('remove_pokeballs_button').set_object_style('normal')

        if len(pokemon_list) == pokemon_number:
            self.get_object(
                'add_pokemon_button').set_object_style('inactive')
            self.get_object(
                'remove_pokeballs_button').set_object_style('inactive')
        else:
            self.get_object(
                'continue_button').set_object_style('inactive')
        if pokemon_number == 1:
            self.get_object(
                'remove_pokeballs_button').set_object_style('inactive')
        elif pokemon_number == 6:
            self.get_object(
                'add_pokeballs_button').set_object_style('inactive')

    def bot_init(self, database: list[BasePokemon]):
        self._set_given_player_pokemon_number(
            self.get_given_player_pokemon_number(1), 2
        )
        pokemon_list = []
        for _ in range(self.get_given_player_pokemon_number(2)):
            pokemon_list.append(GamePokemon(choice(database)))
        self._set_given_player_pokemon_list(pokemon_list, 2)

    def bot_move(self):
        bot_pokemon = self.get_given_player_active_pokemon(2)
        if bot_pokemon.get_is_alive() is False:
            self.remove_pokemon_from_player(bot_pokemon, 2)
            self.set_given_player_active_pokemon(randint(0, len(
                self.get_given_player_poke_list(2)) - 1), 2)
            self.change_given_player_frame(2)
        else:
            player_pokemon = self.get_given_player_active_pokemon(1)
            random = randint(0, 100)
            defend_threshold = bot_pokemon.get_hp() / float(
                bot_pokemon.get_max_hp()) / 2 * 100
            special_threshold = bot_pokemon.get_special_type_multiplier(
                player_pokemon) * 4 * 6

            if random > defend_threshold:
                self.attack_pokemon_handle(2)
            elif random > special_threshold:
                self.block_pokemon_handle(2)
            else:
                self.special_pokemon_handle(2)

    def game_init_finish(self):
        self.set_given_player_active_pokemon(0, 1)
        self.set_given_player_active_pokemon(0, 2)
        self.set_game_state('game')
        self._draw_starting_turn()
        self.get_exact_object(
            'game', 'player_one', 'player_one_frame').set_active_pokemon(
                self.get_given_player_poke_list(1)[0]
            )
        self.get_exact_object(
            'game', 'player_one', 'player_two_frame').set_active_pokemon(
                self.get_given_player_poke_list(2)[0]
            )
        self.get_exact_object(
            'game', 'player_two', 'player_one_frame').set_active_pokemon(
                self.get_given_player_poke_list(1)[0]
            )
        self.get_exact_object(
            'game', 'player_two', 'player_two_frame').set_active_pokemon(
                self.get_given_player_poke_list(2)[0]
            )

    def add_pokemon_popup(
            self, tk_window: TkPokemonSelectWindow, player: int) -> None:
        tk_window.show_window()
        if tk_window.get_choosen_pokemon():
            add_pok = tk_window.get_choosen_pokemon()
            add_pok = GamePokemon(add_pok)
            self.add_pokemon_to_player(add_pok, player)
            game_list = self.get_object('pokemon_list')
            game_list.add_elem_to_list(add_pok)
            self.game_init_handle('add_pokemon_button', player)

    def _draw_starting_turn(self) -> None:
        player_one_starting_pokemon_spd = self.get_given_player_poke_list(
            1)[0].get_speed()
        player_two_starting_pokemon_spd = self.get_given_player_poke_list(
            2)[0].get_speed()
        if player_one_starting_pokemon_spd >= player_two_starting_pokemon_spd:
            self.set_player_turn(1)
            self.set_menu_state('player_one')
        else:
            self.set_player_turn(2)
            self.set_menu_state('player_two')

    def set_given_player_active_pokemon(self,
                                        list_index: int | None,
                                        player: int):
        if player == 1:
            self._player_one_active_pokemon = self.get_given_player_poke_list(
                player)[list_index] if not isinstance(
                    list_index, type(None)) else None
        else:
            self._player_two_active_pokemon = self.get_given_player_poke_list(
                player)[list_index] if not isinstance(
                    list_index, type(None)) else None

    def get_given_player_active_pokemon(self, player: int) -> GamePokemon:
        if player == 1:
            return self._player_one_active_pokemon
        else:
            return self._player_two_active_pokemon

    def get_player_turn(self) -> int:
        return self._player_turn

    def set_player_turn(self, active_player: int) -> None:
        self._player_turn = active_player

    def game_init_reset(self) -> None:
        self.set_real_players_count(None)
        self._selected_pokemon = None
        self._selected_frame = None
        self._set_given_player_pokemon_number(1, 1)
        self._set_given_player_pokemon_list([], 1)
        self._set_given_player_pokemon_number(1, 2)
        self._set_given_player_pokemon_list([], 2)
        self.get_exact_object(
            'game_init', 'player_one_init', 'pokemon_list').clear_objects()
        self.get_exact_object(
            'game_init', 'player_one_init',
            'remove_pokemon_button').set_object_style('inactive')
        self.get_exact_object(
            'game_init', 'player_two_init', 'pokemon_list').clear_objects()
        self.get_exact_object(
            'game_init', 'player_two_init',
            'remove_pokemon_button').set_object_style('inactive')

    def game_reset(self):
        self.set_given_player_active_pokemon(None, 1)
        self.set_given_player_active_pokemon(None, 2)
        self._winner = None
        self.game_init_reset()

    def pause_resume(self):
        if self.get_player_turn() == 1:
            self.set_menu_state('player_one')
        else:
            self.set_menu_state('player_two')

    def list_select_item(self, list_elem: PokemonListElem) -> None:
        if list_elem.get_event_type() == 'Select':
            for elem_check in self.get_list_elems(
                    'pokemon_list'):
                if not elem_check.raise_event():
                    elem_check.deselect_elem()
            self.get_object(
                'remove_pokemon_button'
                ).set_object_style('normal')
            self.set_selected_pokemon(
                list_elem.get_elem_object()
                )
            self.set_selected_frame(list_elem)
        elif list_elem.get_event_type() == 'Deselect':
            self.get_object(
                'remove_pokemon_button'
                ).set_object_style('inactive')
            self.set_selected_pokemon(None)
            self.set_selected_frame(None)

    def get_given_player_poke_list(self, player: int):
        if player == 1:
            return self._player_one_pokemons
        else:
            return self._player_two_pokemons

    def _set_given_player_pokemon_list(
            self, value: list[GamePokemon], player: int):
        if player == 1:
            self._player_one_pokemons = value
        else:
            self._player_two_pokemons = value

    def get_given_player_pokemon_number(self, player: int):
        if player == 1:
            return self._player_one_pokemon_number
        else:
            return self._player_two_pokemon_number

    def _set_given_player_pokemon_number(self, value, player: int):
        if player == 1:
            self._player_one_pokemon_number = value
        else:
            self._player_two_pokemon_number = value

    def get_selected_pokemon(self) -> GamePokemon | None:
        return self._selected_pokemon

    def set_selected_pokemon(self, pokemon: GamePokemon) -> None:
        self._selected_pokemon = pokemon

    def get_selected_frame(self) -> PokemonListElem | None:
        return self._selected_frame

    def set_selected_frame(self, frame: PokemonListElem) -> None:
        self._selected_frame = frame

    def add_pokemon_to_player(self, pokemon: GamePokemon, player):
        pokemons = self.get_given_player_poke_list(player)
        pokemons.append(pokemon)
        self._set_given_player_pokemon_list(pokemons, player)

    def remove_pokemon_from_player(self, pokemon: GamePokemon, player):
        pokemons = self.get_given_player_poke_list(player)
        for idx, elem in enumerate(pokemons):
            if elem == pokemon:
                pokemons.pop(idx)
                break
        self._set_given_player_pokemon_list(pokemons, player)

    def get_real_players_count(self):
        return self._player_count

    def get_list_elems(self, object_key) -> list[PokemonListElem]:
        object = self.get_active_objects()[object_key]
        return object.get_elem_list()

    def get_object(self, object_key):
        active_objects = self.get_active_objects()
        try:
            object = active_objects[object_key]
            return object
        except KeyError:
            raise RedundantKeyError('Given object does not exist')

    def get_exact_object(self, game_state, menu_state, object_key):
        try:
            return self._objects_database.get_active_objects(
                game_state, menu_state)[object_key]
        except KeyError:
            raise RedundantKeyError('Given object does not exist')

    def raised_event(self, object_key) -> bool:
        try:
            object = self.get_object(object_key)
            return object.raise_event()
        except Exception:
            return False

    def get_active_objects(self):
        return self._objects_database.get_active_objects(
            self.get_game_state(), self.get_menu_state()
        )

    def get_winner(self):
        return self._winner

    def get_game_state(self):
        return self._game_state

    def get_menu_state(self):
        return self._menu_state

    def set_game_state(self, game_state):
        self._game_state = game_state

    def set_menu_state(self, menu_state):
        self._menu_state = menu_state

    def set_real_players_count(self, players: int) -> None:
        self._player_count = players

    def update_turn(self, player: int) -> None:
        if player == 1:
            self.set_player_turn(2)
            self.set_menu_state('player_two')
        else:
            self.set_player_turn(1)
            self.set_menu_state('player_one')
        self.get_object('game_pokemon_list').set_is_visible(False)
        self.get_object('special_list').set_is_visible(False)

    # MAIN GAME FUNCTIONS:

    def _get_pokemons_and_enemy(self, player) -> tuple[
            int, GamePokemon, GamePokemon]:
        if player == 1:
            enemy = 2
        else:
            enemy = 1
        p_pokemon = self.get_given_player_active_pokemon(player)
        e_pokemon = self.get_given_player_active_pokemon(enemy)
        return (enemy, p_pokemon, e_pokemon)

    def attack_pokemon_handle(self, player: int):
        enemy, p_pokemon, e_pokemon = self._get_pokemons_and_enemy(player)
        p_pokemon.attack_basic(e_pokemon)
        self.get_object('attack_button').reset_event()
        self.update_turn(player)
        if e_pokemon.get_is_alive() is False:
            self._dead_pokemon_handle(player, enemy)

    def block_pokemon_handle(self, player: int):
        pokemon = self.get_given_player_active_pokemon(player)
        pokemon.increase_defense()
        self.get_object('block_button').reset_event()
        self.update_turn(player)

    def special_pokemon_handle(self, player: int):
        enemy, p_pokemon, e_pokemon = self._get_pokemons_and_enemy(player)
        p_pokemon.attack_special(e_pokemon)
        for elem in self.get_object('special_list').get_elem_list():
            elem.reset_event()
        self.update_turn(player)

        if e_pokemon.get_is_alive() is False:
            self._dead_pokemon_handle(player, enemy)

    def _dead_pokemon_handle(self, player: int, enemy: int):
        self.get_object('game_pokemon_list').set_elem_list(
                    self.get_given_player_poke_list(enemy)
                )
        self._set_given_player_pokemon_number(
            self.get_given_player_pokemon_number(enemy) - 1, enemy)
        if self.get_given_player_pokemon_number(enemy) == 0:
            self.draw_winner(player)
        else:
            self._deactivate_game_buttons()
            self.get_object('game_pokemon_list').set_is_visible(True)

    def _deactivate_game_buttons(self):
        self.get_object('attack_button').set_object_style('big_inactive')
        self.get_object('special_button').set_object_style('big_inactive')
        self.get_object('block_button').set_object_style('big_inactive')

    def _activate_game_buttons(self):
        self.get_object('attack_button').set_object_style('big')
        self.get_object('special_button').set_object_style('big')
        self.get_object('block_button').set_object_style('big')

    def draw_winner(self, winner: int):
        self._winner = winner
        self.set_menu_state('finish')

    def change_pokemon_handle(self, pokemon: GamePokemon, player: int):
        pokemon_list = self.get_given_player_poke_list(player)
        for idx, pok in enumerate(pokemon_list):
            if pok == pokemon:
                self.set_given_player_active_pokemon(idx, player)
                break
        else:
            raise PokemonDataDoesNotExistError(
                'Given pokemon is not in player list'
                )
        self._activate_game_buttons()
        for elem in self.get_object('game_pokemon_list').get_elem_list():
            elem.reset_event()
        self.change_given_player_frame(player)

    def change_given_player_frame(self, player: int) -> None:
        if player == 1:
            self.get_exact_object(
                'game', 'player_one', 'player_one_frame').set_active_pokemon(
                    self.get_given_player_active_pokemon(1)
                )
            self.get_exact_object(
                'game', 'player_two', 'player_one_frame').set_active_pokemon(
                    self.get_given_player_active_pokemon(1)
                )
        else:
            self.get_exact_object(
                'game', 'player_one', 'player_two_frame').set_active_pokemon(
                    self.get_given_player_active_pokemon(2)
                )
            self.get_exact_object(
                'game', 'player_two', 'player_two_frame').set_active_pokemon(
                    self.get_given_player_active_pokemon(2)
                )
        self.update_turn(player)


def main():
    run = True
    screen = Screen()
    game = PokemonGame()
    tk_sel_window = TkPokemonSelectWindow()
    text_database = TextDatabase()
    while run:
        screen.get_clock().tick(FPS)

        # Game widget events
        g_state = game.get_game_state()
        m_state = game.get_menu_state()

        if g_state == 'main_menu':
            if m_state == 'main_menu':
                if game.raised_event('play_button'):
                    game.set_menu_state('players_select')
                elif game.raised_event('credits_button'):
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
                    game.set_real_players_count(1)
                    game.game_init_handle(None, 1)
                elif game.raised_event('2_player_button'):
                    game.set_game_state('game_init')
                    game.set_menu_state('player_one_init')
                    game.set_real_players_count(2)
                    game.game_init_handle(None, 1)
                elif game.raised_event('back_button'):
                    game.set_menu_state('main_menu')

        elif g_state == 'game_init':
            if m_state == 'player_one_init':

                for elem in game.get_list_elems('pokemon_list'):
                    if elem.raise_event():
                        game.list_select_item(elem)

                if game.raised_event('add_pokemon_button'):
                    game.add_pokemon_popup(tk_sel_window, 1)

                elif game.raised_event('remove_pokemon_button'):
                    object_list = game.get_object('pokemon_list')
                    selected = game.get_selected_frame()
                    object_list.remove_selected_object(selected)
                    game.remove_pokemon_from_player(
                        game.get_selected_pokemon(), 1
                        )
                    game.game_init_handle('remove_pokemon_button', 1)

                elif game.raised_event('add_pokeballs_button'):
                    game.game_init_handle('add_pokeballs_button', 1)

                elif game.raised_event('remove_pokeballs_button'):
                    game.game_init_handle('remove_pokeballs_button', 1)

                elif game.raised_event('back_button'):
                    game.get_object('pokemon_list').clear_objects()
                    game.game_init_reset()
                    game.set_menu_state('main_menu')
                    game.set_game_state('main_menu')

                elif game.raised_event('continue_button'):
                    if game.get_real_players_count() == 2:
                        game.set_menu_state('player_two_init')
                        game.game_init_handle(None, 2)
                    else:
                        game.bot_init(tk_sel_window.get_full_database())
                        game.set_menu_state('start_game')
                        pass

            elif m_state == 'player_two_init':
                for elem in game.get_list_elems('pokemon_list'):
                    if elem.raise_event():
                        game.list_select_item(elem)

                if game.raised_event('add_pokemon_button'):
                    game.add_pokemon_popup(tk_sel_window, 2)

                elif game.raised_event('remove_pokemon_button'):
                    object_list = game.get_object('pokemon_list')
                    selected = game.get_selected_frame()
                    object_list.remove_selected_object(selected)
                    game.remove_pokemon_from_player(
                        game.get_selected_pokemon(), 2
                        )
                    game.game_init_handle('remove_pokemon_button', 2)

                elif game.raised_event('continue_button'):
                    game.set_menu_state('start_game')

                elif game.raised_event('add_pokeballs_button'):
                    game.game_init_handle('add_pokeballs_button', 2)

                elif game.raised_event('remove_pokeballs_button'):
                    game.game_init_handle('remove_pokeballs_button', 2)

                elif game.raised_event('back_button'):
                    game.get_object('pokemon_list').clear_objects()
                    game.game_init_reset()
                    game.set_menu_state('main_menu')
                    game.set_game_state('main_menu')

            elif m_state == 'start_game':
                if game.raised_event('start'):
                    game.game_init_finish()

        elif g_state == 'game':
            if m_state == 'player_one':
                for special_elem in game.get_object(
                        'special_list').get_elem_list():
                    if special_elem.raise_event():
                        game.special_pokemon_handle(1)
                for pokemon_elem in game.get_object(
                        'game_pokemon_list').get_elem_list():
                    if pokemon_elem.raise_event():
                        game.change_pokemon_handle(
                            pokemon_elem.get_elem_object(), 1)
                if game.raised_event('attack_button'):
                    game.attack_pokemon_handle(1)
                elif game.raised_event('special_button'):
                    game.get_object('special_list').set_elem_list(
                        game.get_given_player_active_pokemon(1)
                    )
                    game.get_object('game_pokemon_list').set_is_visible(False)
                    game.get_object('special_list').set_is_visible(
                        not game.get_object('special_list').get_is_visible()
                    )
                elif game.raised_event('block_button'):
                    game.block_pokemon_handle(1)
                elif game.raised_event('change_pokemon_button'):
                    game.get_object('game_pokemon_list').set_elem_list(
                        game.get_given_player_poke_list(1)
                    )
                    game.get_object('special_list').set_is_visible(False)
                    game.get_object('game_pokemon_list').set_is_visible(
                        not game.get_object(
                            'game_pokemon_list').get_is_visible()
                    )

            elif m_state == 'player_two':
                if game.get_real_players_count() == 2:
                    for pokemon_elem in game.get_object(
                            'game_pokemon_list').get_elem_list():
                        if pokemon_elem.raise_event():
                            game.change_pokemon_handle(
                                pokemon_elem.get_elem_object(), 2)
                    for special_elem in game.get_object(
                            'special_list').get_elem_list():
                        if special_elem.raise_event():
                            game.special_pokemon_handle(2)
                    if game.raised_event('attack_button'):
                        game.attack_pokemon_handle(2)
                    elif game.raised_event('special_button'):
                        game.get_object('special_list').set_elem_list(
                            game.get_given_player_active_pokemon(2)
                        )
                        game.get_object(
                            'game_pokemon_list').set_is_visible(False)
                        game.get_object('special_list').set_is_visible(
                            not game.get_object(
                                'special_list').get_is_visible()
                        )
                    elif game.raised_event('block_button'):
                        game.block_pokemon_handle(2)

                    elif game.raised_event('change_pokemon_button'):
                        game.get_object('game_pokemon_list').set_elem_list(
                            game.get_given_player_poke_list(2)
                        )
                        game.get_object('special_list').set_is_visible(False)
                        game.get_object('game_pokemon_list').set_is_visible(
                            not game.get_object(
                                'game_pokemon_list').get_is_visible()
                        )

            elif m_state == 'pause':
                if game.raised_event('continue_button'):
                    game.pause_resume()
                elif game.raised_event('main_menu_button'):
                    game.game_reset()
                    game.set_game_state('main_menu')
                    game.set_menu_state('main_menu')
                elif game.raised_event('quit_button'):
                    run = False

            elif m_state == 'finish':
                if game.raised_event('continue_button'):
                    game.game_reset()
                    game.set_game_state('main_menu')
                    game.set_menu_state('main_menu')

            if game.get_menu_state() == 'player_two':
                if game.get_real_players_count() == 1:
                    game.bot_move()
                    if game.get_menu_state() != 'finish':
                        game.set_menu_state('player_one')
        # Game draw static objects

        g_state = game.get_game_state()
        m_state = game.get_menu_state()
        objects = game.get_active_objects()
        screen.draw_bg()

        if g_state == 'main_menu':
            if m_state == 'main_menu':
                screen.draw_clear_text((399, 150), "Pokemon game",
                                       font="BIG_FONT")
            elif m_state == 'credits_menu':
                text_credits = text_database.get_text('credits')
                screen.draw_multiline_text(
                    (399, 200), text_credits
                    )
            elif m_state == 'players_select':
                pass
        elif g_state == 'game_init':
            if m_state == 'player_one_init':
                screen.draw_balls(
                    game.get_object('pokeballs'),
                    game.get_given_player_pokemon_number(1)
                )
            elif m_state == 'player_two_init':
                screen.draw_balls(
                    game.get_object('pokeballs'),
                    game.get_given_player_pokemon_number(2)
                )
            elif m_state == 'start_game':
                pass
        elif g_state == 'game':
            if m_state == 'player_one':
                pygame.draw.line(screen._get_screen(), (255, 255, 255),
                                 (0, 400), (800, 400), 3)
                screen.draw_clear_text((400, 500), "P1")
            elif m_state == 'player_two':
                pygame.draw.line(screen._get_screen(), (255, 255, 255),
                                 (0, 400), (800, 400), 3)
                screen.draw_clear_text((400, 500), "P2")
            elif m_state == 'pause':
                screen.draw_clear_text((399, 180), "Pause",
                                       font="BIG_FONT")
            elif m_state == 'finish':
                winner_val = game.get_winner()
                winnet_text = 'Winner: Player {}'.format(
                    winner_val if not isinstance
                    (winner_val, type(None)) else 'Unknown')

                screen.draw_clear_text((400, 200), winnet_text,
                                       'BIG_FONT')

        screen.draw_objects(objects)
        screen.update_display()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if g_state == 'game':
                        if m_state == 'player_one':
                            game.set_menu_state('pause')
                        elif m_state == 'player_two':
                            game.set_menu_state('pause')
                        elif m_state == 'pause':
                            game.pause_resume()
    pygame.quit()


if __name__ == '__main__':
    main()
