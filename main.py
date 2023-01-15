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
from typing import Literal
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
    PokemonDataDoesNotExistError,
    InvalidObjectTypeError,

)

from model_io import check_if_valid_key
from tk_objects import TkPokemonSelectWindow
from database import PyGameObjectsDatabase, TextDatabase
from classes import BasePokemon, GamePokemon


pygame.init()


class Screen:
    """PyGame screen window class with embedded drawing functions.
    """
    def __init__(self) -> None:
        """Initialises main screen with basic parameters set in attributes.
        """
        self._screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), flags=0)
        self._clock = pygame.time.Clock()
        pygame.display.set_caption("Pokemon - Mateusz Bojarski")

    # Main functions

    def draw_bg(self):
        """ Draws screen background.
        """
        self._get_screen().fill(COLORS.get('BG_COLOR'))

    def update_display(self):
        """Updates current pygame display
        """
        pygame.display.update()

    # Objects select

    def draw_objects(self, objects_dict: dict[str]) -> None:
        """Gets every single object type and handles it by it's name.

        Args:
            objects_dict (dict[str]): Dict with every active PyGame object.
        """
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

    # Objects handle

    def _draw_game_pokemon_list(self, list_object: GamePokemonList) -> None:
        """Gets GamePokemonList object and draws it visible flag is True.
        Otherwise resets events in itself.

        Args:
            list_object (GamePokemonList): List of playing pokemons.
        """
        if list_object.get_is_visible():
            self._draw_list(list_object)
        else:
            for elem in list_object.get_elem_list():
                elem._raise_event = False

    def _draw_special_list(self, list_object: SpecialList) -> None:
        """Draws SpecialList with it's elements if it's visible.

        Args:
            list_object (SpecialList): SpecialList object
        """
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
        """Draw PokemonList with it's values on the screen.

        Args:
            list_object (PokemonList): PokemonLit object.
        """
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
        """ Draws main game's frame on the screen.

        Args:
            frame_object (PokemonFrame): PokemonFrame object.
        """
        screen = self._get_screen()
        draw_val = frame_object.get_draw_values()
        image = draw_val[0]
        texts = draw_val[1]
        screen.blit(image[0], image[1])
        for text in texts:
            screen.blit(text[0], text[1])

    def _draw_button(self, button_object: Button) -> None:
        """ Draws PyGame's button on the screen.

        Args:
            button_object (Button): Button PyGame object.
        """
        screen = self._get_screen()
        draw_val = button_object.get_draw_values()
        pygame.draw.rect(screen, draw_val[0],
                         draw_val[1], border_radius=12)
        pygame.draw.rect(screen, draw_val[2],
                         pygame.Rect(draw_val[3]), 3, border_radius=12)
        screen.blit(draw_val[4], draw_val[5])

    def draw_balls(self, object: PokemonBalls, count: int) -> None:
        """ Draws how many PokeBalls are active on the screen

        Args:
            object (PokemonBalls): PokemonBalls PyGame object
            count (int): How many pokeballs are active
        """
        screen = self._get_screen()
        draw_vals = object.get_draw_values(count)
        for elem in draw_vals:
            screen.blit(elem[0], elem[1])

    # Checking functions

    def _check_if_valid_text_args(
            self,
            font: Literal['GUI_FONT', 'BIG_FONT', 'MEDIUM_FONT',
                          'SMALL_FONT', 'SMALLER_FONT'],
            color: str,
            align: Literal['center', 'left', 'right']):

        """Checks if given text values are valid. Throws exception
        if one of them isn't.

        Args:
            font (str): Text font to check.
            color (str): Text color to check.
            align (str): Text alignment to check.

        Raises:
            RedundantKeyError: Given key is invalid.
            BadConversionError: Given text is not a string.
        """
        try:
            check_if_valid_key(align, ['center', 'left', 'right'])
            check_if_valid_key(font, FONTS.keys())
            check_if_valid_key(color, COLORS.keys())
        except RedundantKeyError:
            raise RedundantKeyError('Given key is invalid.')

    # Clear text functions

    def draw_clear_text(
            self,
            pos: tuple[float, float],
            text: str,
            font: Literal['GUI_FONT', 'BIG_FONT', 'MEDIUM_FONT',
                          'SMALL_FONT', 'SMALLER_FONT'] = 'MEDIUM_FONT',
            color: str = 'INPURE_WHITE',
            align: Literal['center', 'left', 'right'] = 'center'
            ):
        """Draws clear text without objects from saved value

        Args:
            pos (tuple): Text's position
            text (str): Text to display
            font (str, optional): Text font.
            Defaults to 'MEDIUM_FONT'.
            color (str, optional): Text color.
            Defaults to 'INPURE_WHITE'.
            align (str, optional): Text alignment.
            Defaults to 'center'.

        Raises:
            RedundantKeyError: Given key is invalid.
        """
        try:
            self._check_if_valid_text_args(font, color, align)
        except RedundantKeyError:
            raise RedundantKeyError('Given key is invalid.')
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
            self,
            pos: tuple[float, float],
            text_lines,
            fsize: int = 40,
            font: Literal['GUI_FONT', 'BIG_FONT', 'MEDIUM_FONT',
                          'SMALL_FONT', 'SMALLER_FONT'] = 'MEDIUM_FONT',
            color: str = 'INPURE_WHITE',
            align: Literal['center', 'left', 'right'] = 'center'
            ):
        """Draws list of texts without objects from saved value

        Args:
            pos (tuple): Text's position
            text_lines (str): List of texts to display
            font (str, optional): Text font.
            fsize (int, optional): Distance between lines.
            Defaults to 40.
            Defaults to 'MEDIUM_FONT'.
            color (str, optional): Text color.
            Defaults to 'INPURE_WHITE'.
            align (str, optional): Text alignment.
            Defaults to 'center'.

        Raises:
            RedundantKeyError: Given key is invalid.
        """

        for idx, line in enumerate(text_lines):
            pos_x = pos[0]
            pos_y = pos[1] + idx * fsize
            self.draw_clear_text((pos_x, pos_y), line, font, color, align)

    # Getters

    def get_clock(self) -> pygame.time.Clock:
        """Gets private value of screen's clock (FPS) and returns it

        Returns:
            pygame.time.Clock: Active clock object
        """
        return self._clock

    # Private getters

    def _get_screen(self) -> pygame.display:
        """Gets private value of screen display object and returns it

        Returns:
            pygame.display: Active display
        """
        return self._screen


class PokemonGame:
    """Main game handle
    """
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

    # MAIN GAME FUNCTIONS

    def raised_event(self, object_key: str) -> bool:
        """Gets if given object raised event.

        Args:
            object_key (str): Given object from active game and menu state.

        Returns:
            bool: Is event raised or False if key is invalid.
        """
        try:
            object = self.get_object(object_key)
            return object.raise_event()
        except Exception:
            return False

    # # Init

    def game_init_handle(self, object_type: str | None, player: int) -> None:
        """Creates init screen logic with given objct type and player.

        Args:
            object_type (str | None): Given object's event.
            player (int): Player's number.
        """

        # Objects handle

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

        # Reset init button states

        self.get_object('continue_button').set_object_style('normal')
        self.get_object('add_pokemon_button').set_object_style('normal')
        self.get_object('add_pokeballs_button').set_object_style('normal')
        self.get_object('remove_pokeballs_button').set_object_style('normal')

        # Deactivates buttons that cannot be pressed

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

    def add_pokemon_popup(self,
                          tk_window: TkPokemonSelectWindow,
                          player: int) -> None:
        """_summary_

        Args:
            tk_window (TkPokemonSelectWindow): Window class
            player (int): Player's number

        Raises:
            InvalidObjectTypeError: Given object is not a window.
        """
        if not isinstance(tk_window, TkPokemonSelectWindow):
            raise InvalidObjectTypeError('Given object is not a window.')
        tk_window.show_window()
        if tk_window.get_choosen_pokemon():
            add_pok = tk_window.get_choosen_pokemon()
            add_pok = GamePokemon(add_pok)
            self.add_pokemon_to_player(add_pok, player)
            game_list = self.get_object('pokemon_list')
            game_list.add_elem_to_list(add_pok)
            self.game_init_handle('add_pokemon_button', player)

    def game_init_finish(self):
        """Finishes game init using saved values
        """
        # Active pokemons and state
        self.set_given_player_active_pokemon(0, 1)
        self.set_given_player_active_pokemon(0, 2)
        self.set_game_state('game')

        # Draw who starts first
        self._draw_starting_turn()

        # Update frames
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

    # # Game

    def attack_pokemon_handle(self, player: int):
        """ Attacks pokemon with given player's pokemon to opposing one.
        Triggers dead pokemon handle if given attack is fatal and updates
        turn after attack.

        Args:
            player (int): Player's number
        """
        enemy, p_pokemon, e_pokemon = self._get_pokemons_and_enemy(player)
        p_pokemon.attack_basic(e_pokemon)
        self.get_object('attack_button').reset_event()
        self.update_turn(player)
        if e_pokemon.get_is_alive() is False:
            self._dead_pokemon_handle(player, enemy)

    def block_pokemon_handle(self, player: int):
        """ Increases given player's active pokemon defense.
        Updates turn after block.

        Args:
            player (int): Player's number
        """
        pokemon = self.get_given_player_active_pokemon(player)
        pokemon.increase_defense()
        self.get_object('block_button').reset_event()
        self.update_turn(player)

    def special_pokemon_handle(self, player: int):
        """ Attacks pokemon with given player's pokemon to opposing one
        using speical types.
        Triggers dead pokemon handle if given attack is fatal and updates
        turn after attack.

        Args:
            player (int): Player's number
        """
        enemy, p_pokemon, e_pokemon = self._get_pokemons_and_enemy(player)
        p_pokemon.attack_special(e_pokemon)
        for elem in self.get_object('special_list').get_elem_list():
            elem.reset_event()
        self.update_turn(player)

        if e_pokemon.get_is_alive() is False:
            self._dead_pokemon_handle(player, enemy)

    def change_pokemon_handle(self, pokemon: GamePokemon, player: int):
        """ Changes pokemon to a selected one if it's alive. Updates
        turn after changing pokemons.

        Args:
            pokemon (GamePokemon): Given player's GamePokemon
            player (int): Player's number

        Raises:
            PokemonDataDoesNotExistError: Given pokemon is not in player list.
        """
        pokemon_list = self.get_given_player_poke_list(player)
        for idx, pok in enumerate(pokemon_list):
            if pok == pokemon:
                if pok != self.get_given_player_active_pokemon(player):
                    self.set_given_player_active_pokemon(idx, player)
                    self._activate_game_buttons()
                    for elem in self.get_object(
                            'game_pokemon_list').get_elem_list():
                        elem.reset_event()
                    self.change_given_player_frame(player)
                break
        else:
            raise PokemonDataDoesNotExistError(
                'Given pokemon is not in player list'
                )

    def update_turn(self, player: int) -> None:
        """ Update's turn insie game using currently playing player number.

        Args:
            player (int): Active player number.
        """
        if player == 1:
            self.set_player_turn(2)
            self.set_menu_state('player_two')
        else:
            self.set_player_turn(1)
            self.set_menu_state('player_one')

        self.get_object('game_pokemon_list').set_is_visible(False)
        self.get_object('special_list').set_is_visible(False)

    def draw_winner(self, winner: int):
        """Sets winner of the game and updates manu state to finish.

        Args:
            winner (int): Which player won the game.
        """
        self._winner = winner
        self.set_menu_state('finish')

    # PRIVATE MAIN FUNCTIONS

    def _get_pokemons_and_enemy(self, player) -> tuple[
            int, GamePokemon, GamePokemon]:
        """Gets value of enemy number, player's and enemy's GamePokemon.

        Args:
            player (_type_): Currently active player's number.

        Returns:
            tuple[int, GamePokemon, GamePokemon]: List with enemy's number,
            player's GamePokemon and enemy's GamePokemon (in order).
        """
        if player == 1:
            enemy = 2
        else:
            enemy = 1
        p_pokemon = self.get_given_player_active_pokemon(player)
        e_pokemon = self.get_given_player_active_pokemon(enemy)
        return (enemy, p_pokemon, e_pokemon)

    def _dead_pokemon_handle(self, player: int, enemy: int):
        """ Handle when attack on enemy's pokemon is fatal.
            Function draw winners if none of enemy's pokemon is alive.
            Else it forces to change active pokemon.

        Args:
            player (int): player's number
            enemy (int): enemy's number
        """
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

    def _draw_starting_turn(self) -> None:
        """Draws who will start game based on players first pokemon speed.
        """
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

    def _deactivate_game_buttons(self):
        """Deactivates all important game buttons if pokemon is dead.
        """
        self.get_object('attack_button').set_object_style('big_inactive')
        self.get_object('special_button').set_object_style('big_inactive')
        self.get_object('block_button').set_object_style('big_inactive')

    def _activate_game_buttons(self):
        """Activates back all of active player's buttons.
        """
        self.get_object('attack_button').set_object_style('big')
        self.get_object('special_button').set_object_style('big')
        self.get_object('block_button').set_object_style('big')

    # Bot functions

    def bot_init(self, database: list[BasePokemon]) -> None:
        """Initialises bot with as many random pokemons as player has.

        Args:
            database (list[BasePokemon]): List of all BasePokemon objects.
        """
        self._set_given_player_pokemon_number(
            self.get_given_player_pokemon_number(1), 2
        )
        pokemon_list = []
        for _ in range(self.get_given_player_pokemon_number(2)):
            pokemon_list.append(GamePokemon(choice(database)))
        self._set_given_player_pokemon_list(pokemon_list, 2)

    def bot_move(self):
        """Calculates which move should bot use or forces change if
           currently active pokemon is dead. Changing pokemons
           if active pokemon is alive is prohibited.
        """
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

    # Game reset functions

    def game_init_reset(self) -> None:
        """Resets all init variables and objects.
        """
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
        """Reset all both game and init variables in game
        """
        self.set_given_player_active_pokemon(None, 1)
        self.set_given_player_active_pokemon(None, 2)
        self._winner = None
        self._player_turn = None
        self.game_init_reset()

    # Other game handling functions

    def change_given_player_frame(self, player: int) -> None:
        """ Updates both menus given player's frame after
        active pokemon change.

        Args:
            player (int): Player's number
        """
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

    def pause_resume(self):
        """ Unpauses game using to saved player's turn.
        """
        if self.get_player_turn() == 1:
            self.set_menu_state('player_one')
        else:
            self.set_menu_state('player_two')

    def list_select_item(self, list_elem: PokemonListElem) -> None:
        """Handles if given PokemonListElem object is selected.
        Function depends on saved event type.

        Args:
            list_elem (PokemonListElem): Object that raised event.
        """
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

    def add_pokemon_to_player(self, pokemon: GamePokemon, player: int):
        """Adds GamePokemon to given player's pokemon list.

        Args:
            pokemon (GamePokemon): GamePokemon to add to list
            player (int): Plyer's number
        """
        pokemons = self.get_given_player_poke_list(player)
        pokemons.append(pokemon)
        self._set_given_player_pokemon_list(pokemons, player)

    def remove_pokemon_from_player(self, pokemon: GamePokemon, player):
        """Removes given GamePokemon from given player's pokemon list.
        Does not delete anything if no match is found.

        Args:
            pokemon (GamePokemon): GamePokemon to add to list
            player (int): Player's number
        """
        pokemons = self.get_given_player_poke_list(player)
        for idx, elem in enumerate(pokemons):
            if elem == pokemon:
                pokemons.pop(idx)
                break
        self._set_given_player_pokemon_list(pokemons, player)

    # Getters

    def get_player_turn(self) -> (int | None):
        """Gets private value of current player's turn or None if game
        was not initialised.

        Returns:
            int | None: Which player's turn it is or None if game not
            initalised.
        """
        return self._player_turn

    def get_given_player_active_pokemon(self, player: int) -> GamePokemon:
        """Gets private value given player's active pokemon.

        Args:
            player (int): Player's number.

        Returns:
            GamePokemon: Active GamePokemon object.
        """
        if player == 1:
            return self._player_one_active_pokemon
        else:
            return self._player_two_active_pokemon

    def get_given_player_poke_list(self, player: int) -> list[GamePokemon]:
        """Gets private value given player's pokemons.

        Args:
            player (int): Player's number.

        Returns:
            list[GamePokemon]: List of GamePokemon objects.
        """
        if player == 1:
            return self._player_one_pokemons
        else:
            return self._player_two_pokemons

    def get_given_player_pokemon_number(self, player: int) -> int:
        """Gets private value of given player's pokemon number.
        Value shows how many pokeballs are in player's inventory in game init
        or shows how many pokemons are alive while in main game.

        Args:
            player (int): Player's number.

        Returns:
            list[GamePokemon]: List of GamePokemon objects.
        """
        if player == 1:
            return self._player_one_pokemon_number
        else:
            return self._player_two_pokemon_number

    def get_selected_pokemon(self) -> GamePokemon | None:
        """ Gets private value of currently selected pokemon.

        Returns:
            GamePokemon | None: Selected GamePokemon object.
        """
        return self._selected_pokemon

    def get_selected_frame(self) -> PokemonListElem | None:
        """ Gets private value of currently selected frame.

        Returns:
            PokemonListElem | None: Selected PokemonListElem object.
        """
        return self._selected_frame

    def get_real_players_count(self) -> int | None:
        """ Gets how many players are real or None if game wasn't started.

        Returns:
            int | None: Number of real players.
        """
        return self._player_count

    def get_list_elems(self, object_key: str) -> list[PokemonListElem]:
        """Gets all elements from PokemonList object.
        Throws exception if given key is invalid.

        Args:
            object_key (str): Key corrseponding to pokemon list.

        Raises:
            RedundantKeyError: Given key does not correspond
            to PokemonList object.

        Returns:
            list[PokemonListElem]: List of all PokemonListElems in PokemonList.
        """
        try:
            object = self.get_active_objects()[object_key]
            return object.get_elem_list()
        except Exception:
            raise RedundantKeyError(
                'Given key does not correspond to PokemonList object.'
            )

    def get_object(self, object_key: str):
        """Gets given object from active objects in given game and menu state.
        Throws exception if key is invalid.

        Args:
            object_key (str): Object key.

        Raises:
            RedundantKeyError: Given object key is invalid.

        Returns:
            Any: Any of pygame_classes objects.
        """
        active_objects = self.get_active_objects()
        try:
            object = active_objects[object_key]
            return object
        except KeyError:
            raise RedundantKeyError('Given object does not exist')

    def get_exact_object(self, game_state: str,
                         menu_state: str, object_key: str):
        """Gets given object from exact game and menu state arguments.
        Throws exception if any of given keys is invalid.

        Args:
            game_state (str): Game state.
            menu_state (str): Menu state corresponding to given game state.
            object_key (str): Object key corresponding to given menu state.

        Raises:
            RedundantKeyError: Given object key is invalid.

        Returns:
            Any: Any of pygame_classes objects.
        """
        try:
            return self._objects_database.get_active_objects(
                game_state, menu_state)[object_key]
        except KeyError:
            raise RedundantKeyError('Given object does not exist')

    def get_active_objects(self) -> dict:
        """Gets currently active objects and return dict with them.

        Returns:
            dict: Dict with all objects in given game and menu state
        """
        return self._objects_database.get_active_objects(
            self.get_game_state(), self.get_menu_state()
        )

    def get_winner(self) -> int | None:
        """Gets winner of the game or None if it wans't drawn.

        Returns:
            int | None: Game's winner or none if not present.
        """
        return self._winner

    def get_game_state(self) -> str:
        """Gets current game state and returns it as str.

        Returns:
            str: Current game state.
        """
        return self._game_state

    def get_menu_state(self) -> str:
        """Gets current menu state and returns it as str.

        Returns:
            str: Current menu state.
        """
        return self._menu_state

    # Setters

    def set_player_turn(self, active_player: int) -> None:
        """Sets new player's turn.

        Args:
            active_player (int): New active player.
        """
        self._player_turn = active_player

    def set_given_player_active_pokemon(self,
                                        list_index: int,
                                        player: int):
        """Sets active pokemon of given player using it's saved
        pokemon list and list_index.

        Args:
            list_index (int): Index of pokemon in pokemon's list
            player (int): Player who changes it's active pokemon.
        """
        if player == 1:
            self._player_one_active_pokemon = self.get_given_player_poke_list(
                player)[list_index] if not isinstance(
                    list_index, type(None)) else None
        else:
            self._player_two_active_pokemon = self.get_given_player_poke_list(
                player)[list_index] if not isinstance(
                    list_index, type(None)) else None

    def set_game_state(self, game_state: str):
        """Sets current game state to value given in argument.

        Args:
            game_state (str): New game state.
        """
        self._game_state = game_state

    def set_menu_state(self, menu_state):
        """Sets current menu state to value given in argument.

        Args:
            menu_state (str): New menu state.
        """
        self._menu_state = menu_state

    def set_real_players_count(self, players: int) -> None:
        """Sets how many real players (1 or 2) are in the game.

        Args:
            players (int): How many real players are in the game
        """
        self._player_count = players

    def set_selected_pokemon(self, pokemon: GamePokemon) -> None:
        """Sets currently selected pokemon to value given in argument.

        Args:
            pokemon (GamePokemon): GamePokemon object.
        """
        self._selected_pokemon = pokemon

    def set_selected_frame(self, frame: PokemonListElem) -> None:
        """Sets currently selected frame to value given in argument.

        Args:
            frame (GamePokemon): PokemonListElem object.
        """
        self._selected_frame = frame

    # Private setters

    def _set_given_player_pokemon_list(
            self, value: list[GamePokemon], player: int):
        """Sets given player pokemon list to value given in argument.

        Args:
            value (list[GamePokemon]): List of GamePokemon objects
            player (int): Player's number.
        """
        if player == 1:
            self._player_one_pokemons = value
        else:
            self._player_two_pokemons = value

    def _set_given_player_pokemon_number(self, value: int, player: int):
        """Sets given player pokemon number to value given in argument.

        Args:
            value (int): Number of how many pokemons are in init/alive.
            player (int): Player's number.
        """
        if player == 1:
            self._player_one_pokemon_number = value
        else:
            self._player_two_pokemon_number = value


# EVENT MAINLOOP

def main():

    # Initialise main functions and objects

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

        # Button events

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
