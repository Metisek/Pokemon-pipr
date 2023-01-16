import pygame
from typing import Literal


from classes import GamePokemon
from classes import (
    BadConversionError,
    InvalidDataTypeError,
    InvalidDataLineLeghthError,
    NotANumberError,
    RedundantKeyError,
    InvalidObjectTypeError

)
from model_io import (
    io_convert_to_int,
    io_convert_to_float,
    io_return_if_not_negative,
    io_return_if_positive,
    check_if_valid_key
)

from attributes import (
    FRAME_IMAGE,
    COLORS,
    FONTS
)

pygame.init()


class AbstractWidget:
    """Base AbstractWidget object with basic coordinates values
    and widget's size.
    """
    def __init__(self,
                 size: tuple[float, float],
                 pos: tuple[float, float]
                 ) -> None:
        """Initiates object using given 2 float tuples.
        Throws exception if given arguments are invalid

        Args:
            size (tuple[float, float]): Width x Height size in px.
            pos (tuple[float, float]): Left x Top coordinates.

        Raises:
            InvalidDataTypeError: Given value is not a tuple or list.
            InvalidDataLineLeghthError: Given list or tuple size is
            not equal 2.
            BadConversionError: Given float value cannot be mapped to int.
            NotANumberError: Given value is not a number.
            ValueError: Given value is not greater (or equal) 0.
        """
        try:
            size = self._return_if_tuple_or_list_with_size(size, 2)
            pos = self._return_if_tuple_or_list_with_size(pos, 2)
            self._width = io_return_if_not_negative(
                io_convert_to_float(size[0]))
            self._height = io_return_if_not_negative(
                io_convert_to_float(size[1]))
            self._pos_x = io_return_if_positive(
                io_convert_to_float(pos[0]))
            self._pos_y = io_return_if_positive(
                io_convert_to_float(pos[1]))
            self._raise_event = False
        except InvalidDataTypeError:
            raise InvalidDataTypeError('Given values are not iterable.')
        except InvalidDataLineLeghthError:
            raise InvalidDataLineLeghthError(
                'Given tuple size is not equal 2.'
                )
        except BadConversionError:
            raise BadConversionError(
                'Given float value cannot be mapped to int.'
                )
        except NotANumberError:
            raise NotANumberError('Given value is not a number.')
        except ValueError:
            raise ValueError(
                '''Given value is not greater (or equal) 0
                   or size variable is negative.'''
                )

    # Main functions

    def raise_event(self) -> bool:
        """Returns if given object raised event, without specifying it's type

        Returns:
            bool: If object raised event
        """
        return self._raise_event

    def reset_event(self) -> None:
        """ Reset object's event state (changes it to False).
        """
        self._raise_event = False

    # Checking functions:

    def _return_if_tuple_or_list_with_size(
            self,
            object: (list | tuple),
            size: int
            ) -> (list | tuple):
        """ Checks if given tuple size matches given size value.
            Returns objects if it is, throws exception otherwise.

        Args:
            object (list  |  tuple): list or tuple with elements
            size (int): non-negative size of given object to check

        Raises:
            BadConversionError: Given float value cannot be mapped to int.
            NotANumberError: Given size variable is not a number.
            ValueError: Size of given object must not negative.
            InvalidDataTypeError: Given object is not a list or tuple.
            InvalidDataLineLeghthError: Given object size does not match size
            value.

        Returns:
            list | tuple: Object arg.
        """
        try:
            size = io_return_if_not_negative(io_convert_to_int(size))
        except BadConversionError:
            raise BadConversionError(
                'Given float value cannot be mapped to int.'
                )
        except NotANumberError:
            raise NotANumberError('Given size variable is not a number.')
        except ValueError:
            raise ValueError('Size of given object must be not negative.')
        if not isinstance(object, (tuple, list)):
            raise InvalidDataTypeError('Given values are not iterable.')
        if len(object) != size:
            raise InvalidDataLineLeghthError(
                'Given tuple size is not equal {}'.format(size)
                )
        return object

    # Getters

    def get_size(self) -> tuple[float, float]:
        """ Gets both width and height of given widget and returns it

        Returns:
            tuple[float, float]: Width x Height widget parameters
        """
        return (self._width, self._height)

    def get_pos(self) -> tuple[float, float]:
        """ Gets both left and top coordinates of given widget and returns it

        Returns:
            tuple[float, float]: Left x Top coordinates
        """

        return (self._pos_x, self._pos_y)

    # Setters

    def _set_pos(self, new_pos: tuple[float, float]) -> None:
        """Sets Left x Top coordinates of AbstractWidget object

        Args:
            new_pos (tuple[float, float]): New Left x Top coordinates

        Raises:
            InvalidDataTypeError: Given value is not a tuple or list
            InvalidDataLineLeghthError: Given list or tuple size is not equal 2
            NotANumberError: Given value is not a number
            ValueError: Given value is not greater (or equal) 0
        """
        try:
            new_pos = self._return_if_tuple_or_list_with_size(new_pos, 2)
            x_pos = io_return_if_not_negative(io_convert_to_float(new_pos[0]))
            y_pos = io_return_if_not_negative(io_convert_to_float(new_pos[1]))
        except InvalidDataTypeError:
            raise InvalidDataTypeError('Given values are not iterable')
        except InvalidDataLineLeghthError:
            raise InvalidDataLineLeghthError('Given tuple size is not equal 2')
        except NotANumberError:
            raise NotANumberError('Given value is not a number')
        except ValueError:
            raise ValueError('Given value is not greater or equal 0')

        self._pos_x = x_pos
        self._pos_y = y_pos


class AbstractFrame(AbstractWidget):
    """Abstract frame object containing drawable rectangle with frame
        Also contains values with diffrent object modes
    """
    def __init__(self,
                 size: tuple[float, float],
                 pos: tuple[float, float],
                 object_style: Literal[
                     'normal', 'inactive',
                     'big', 'big_inactive',
                     'no_frame', 'no_frame_inactive'] = 'normal'
                 ) -> None:
        """ Inits frame with given position, size and style.

        Args:
            size (tuple[float, float]): w x h constant size of drawable frame.
            pos (tuple[float, float]):  Left x Top position coordinates.
            object_style (str, optional): key for object style.
            Defaults to 'normal'.

        Raises:
            InvalidDataTypeError: Given size or pos is not a tuple or list.
            InvalidDataLineLeghthError: Given list or tuple size is not equal 2
            BadConversionError: Given float value cannot be mapped to int.
            NotANumberError: Given value is not a number.
            ValueError: Given value is not greater (or equal) 0.
            RedundantKeyError: Given object_style key does not exist.
        """
        super().__init__(size, pos)

        self._colors_dict = {
            'normal': {
                'frame_inactive': COLORS.get('LIGHT_GRAY'),
                'frame_active': COLORS.get('INPURE_WHITE'),
                'bg_inactive': COLORS.get('BLUEISH_BLACK'),
                'bg_active': COLORS.get('DARK_BLUE')
            },
            'inactive': {
                'frame_inactive': COLORS.get('DARK_GRAY'),
                'frame_active': COLORS.get('DARK_GRAY'),
                'bg_inactive': COLORS.get('INPURE_BLACK'),
                'bg_active': COLORS.get('INPURE_BLACK')
            },
            'big': {
                'frame_inactive': COLORS.get('LIGHT_GRAY'),
                'frame_active': COLORS.get('INPURE_WHITE'),
                'bg_inactive': COLORS.get('BLUEISH_BLACK'),
                'bg_active': COLORS.get('DARK_BLUE')
            },
            'big_inactive': {
                'frame_inactive': COLORS.get('DARK_GRAY'),
                'frame_active': COLORS.get('DARK_GRAY'),
                'bg_inactive': COLORS.get('INPURE_BLACK'),
                'bg_active': COLORS.get('INPURE_BLACK')
            },
            'no_frame': {
                'frame_inactive': COLORS.get('BLUEISH_BLACK'),
                'frame_active': COLORS.get('DARK_BLUE'),
                'bg_inactive': COLORS.get('BLUEISH_BLACK'),
                'bg_active': COLORS.get('DARK_BLUE'),
                'font_color': COLORS.get('LIGHT_GRAY')
            },
            'no_frame_inactive': {
                'frame_inactive': COLORS.get('INPURE_BLACK'),
                'frame_active': COLORS.get('INPURE_BLACK'),
                'bg_inactive': COLORS.get('INPURE_BLACK'),
                'bg_active': COLORS.get('INPURE_BLACK'),
                'font_color': COLORS.get('DARK_GRAY')
            },
        }

        self._fonts_dict = {
            'normal': FONTS.get('GUI_FONT'),
            'inactive': FONTS.get('GUI_FONT'),
            'big': FONTS.get('MEDIUM_FONT'),
            'big_inactive': FONTS.get('MEDIUM_FONT'),
            'no_frame': FONTS.get('GUI_FONT'),
            'no_frame_inactive': FONTS.get('GUI_FONT'),
        }

        # Init checks

        try:
            check_if_valid_key(object_style, self._colors_dict.keys())
            check_if_valid_key(object_style, self._fonts_dict.keys())
        except RedundantKeyError:
            raise RedundantKeyError('Given button type does not exist')

        # Drawing attributes

        self._object_style = object_style
        self._set_frame_pos()
        self._set_bg_pos()

    # Getters

    def get_color(self, color_key: str) -> tuple[int, int, int]:
        """Gets RGB value from given object style and string key.
        Throws exception if given key is not a string or is invalid.

        Args:
            color_key (str): key for colors dict as str.

        Raises:
            InvalidDataTypeError: Given value is not a string.
            RedundantKeyError: Given key does not exist.

        Returns:
            tuple [int, int, int]: Color as (R, G, B).
        """
        if not isinstance(color_key, str):
            raise InvalidDataTypeError('Given value is not a string')
        style = self.get_object_style()
        keys = self._colors_dict.get(style).keys()
        try:
            check_if_valid_key(color_key, keys)
        except RedundantKeyError:
            raise RedundantKeyError('Given key does not exist')
        return self._colors_dict.get(style).get(color_key)

    def get_object_style(self) -> str:
        """Checks style of given object and returns it as string.

        Returns:
            str: Button type key as string.
        """
        return self._object_style

    def get_font(self) -> pygame.font.Font:
        """Gets font from given button type and returns font object

        Returns:
            pygame.font.SysFont: Pygame font object.
        """
        return self._fonts_dict.get(self.get_object_style())

    def get_frame(self) -> tuple[pygame.Rect, tuple[int, int, int]]:
        """Gets both frame pygame.Rect object and colors tuple and returns it.

        Returns:
            tuple[pygame.Rect, tuple[int, int, int]]: tuple with given values.
        """
        return (self._frame_rect, self._frame_color)

    def get_bg(self) -> tuple[pygame.Rect, tuple[int, int, int]]:
        """Gets both bg pygame.Rect object and colors tuple and returns it.

        Returns:
            tuple[pygame.Rect, tuple[int, int, int]]: tuple with given values.
        """
        return (self._bg_rect, self._bg_color)

    # Setters

    def set_object_style(self,
                         object_style: Literal[
                            'normal', 'inactive',
                            'big', 'big_inactive',
                            'no_frame', 'no_frame_inactive']
                         ) -> None:
        """ Sets given object style to given string key.
            Throws exception if given key is invalid.

        Args:
            object_style (str): Object style for reading fonts and colors keys.

        Raises:
            RedundantKeyError: Given key is invalid.
        """
        try:
            check_if_valid_key(object_style, self._colors_dict.keys())
            check_if_valid_key(object_style, self._fonts_dict.keys())
        except RedundantKeyError:
            raise RedundantKeyError('Given button type does not exist')
        self._object_style = object_style

    # Private setters

    def _set_frame_pos(self) -> None:
        """Sets current frame to saved position
        """
        self._frame_rect = pygame.Rect(self.get_pos(), self.get_size())

    def _set_bg_pos(self) -> None:
        """Sets current background frame to saved position
        """
        self._bg_rect = pygame.Rect(self.get_pos(), self.get_size())

    def _set_frame_color(self, color: tuple[int, int, int]) -> None:
        """Sets current frame color to given RGB value

        Args:
            color (tuple[int, int, int]): (R, G, B) values
        """
        self._frame_color = color

    def _set_bg_color(self, color: tuple[int, int, int]) -> None:
        """Sets current frame background color to given RGB value

        Args:
            color (tuple[int, int, int]): (R, G, B) values
        """
        self._bg_color = color

    # Other

    def change_frame_pos(self, pos: tuple[float, float]) -> None:
        """Sets Left x Top coordinates of frame object and automatically
        moves rectangle do given coordinates

        Args:
            new_pos (tuple[float, float]): New Left x Top coordinates

        Raises:
            InvalidDataTypeError: Given value is not a tuple or list
            InvalidDataLineLeghthError: Given list or tuple size is not equal 2
            NotANumberError: Given value is not a number
            ValueError: Given value is not greater (or equal) 0
        """
        self._set_pos(pos)
        self._set_frame_pos()
        self._set_bg_pos()


class Button(AbstractFrame):
    """ Clickable button object with ability to deactivate it.
    """
    def __init__(self,
                 text: str,
                 size: tuple[float, float],
                 pos: tuple[float, float],
                 object_style: Literal[
                     'normal', 'inactive',
                     'big', 'big_inactive',
                     'no_frame', 'no_frame_inactive'] = 'normal') -> None:
        """ Initialises button with given text, frame and style.

        Args:
            text (str): Text displayed on button
            size (tuple[float, float]): w x h constant size of drawable frame.
            pos (tuple[float, float]):  Left x Top position coordinates.
            object_style (str, optional): key for object style.
            Defaults to 'normal'.

        Raises:
            InvalidDataTypeError: Given size or pos is not a tuple or list,
            or given text is bot str.
            InvalidDataLineLeghthError: Given list or tuple size is not equal 2
            BadConversionError: Given float value cannot be mapped to int.
            NotANumberError: Given value is not a number.
            ValueError: Given value is not greater (or equal) 0.
            RedundantKeyError: Given object_style key does not exist.
        """

        super().__init__(size, pos, object_style)

        # Init checks
        if not isinstance(text, str):
            raise InvalidDataTypeError('Given text is not a string')

        # Core attributes
        self._is_pressed = False

        # Button drawing attributes
        self._original_y_pos = pos[1]
        self._elevation = 2
        self._dynamic_elevation = 2

        # Text:
        self._text = text
        self._text_surf = self.get_font().render(
            text, True, self.get_color('frame_inactive')
        )
        self._text_rect = self._text_surf.get_rect(
            center=self._frame_rect.center
            )

    # Main functions

    def get_draw_values(self) -> tuple[tuple[int, int, int], pygame.Rect,
                                       tuple[int, int, int], pygame.Rect,
                                       pygame.surface.Surface, pygame.Rect]:

        """ Gets draw walues with saved values and frames.
            Fuction also updates colors from check_click function.

        Returns:
            tuple(
                tuple(int,int,int), pygame.Rect, (frame_bg)\n
                tuple(int,int,int), pygame.Rect, (frame_frame)\n
                pygame.surface.Surface, pygame.Rect (frame_text)
                ): tuple with given objects handled within Screen class,
                in order:
            - Button background color
            - Button background Rect object
            - Button frame color
            - Button frame position Rect object
            - Text Surface object
            - Text Rect object
        """
        self._frame_rect.y = self._original_y_pos - self._dynamic_elevation
        self._text_rect.center = self._frame_rect.center
        self._bg_rect.midtop = self._frame_rect.midtop
        self._bg_rect.height = float(self._frame_rect.height
                                     + self._dynamic_elevation)

        self.check_click()

        return (self._bg_color, self._bg_rect,
                self._frame_color, self._frame_rect,
                self._text_surf, self._text_rect)

    def check_click(self) -> None:
        """Function checks if mouse is over button, if it's clicked, and if
        it's raises event for game mainloop
        """
        self._dynamic_elevation = 2
        self._raise_event = False
        if self.get_object_style() == 'inactive' or self.get_object_style(
                ) == 'big_inactive':
            self.set_inactive_button_colors()
        else:
            mouse_pos = pygame.mouse.get_pos()
            if self._frame_rect.collidepoint(mouse_pos):
                self.set_active_button_colors()
                if pygame.mouse.get_pressed()[0]:
                    self._dynamic_elevation = 0
                    self._is_pressed = True
                    self.set_text(self.get_button_text())
                else:
                    self._dynamic_elevation = self._elevation
                    if self._is_pressed is True:
                        self._raise_event = True
                        self._is_pressed = False
                        self.set_text(self.get_button_text())
            else:
                self._is_pressed = False
                self.set_inactive_button_colors()
                self._dynamic_elevation = self._elevation

    # Getters

    def get_button_is_pressed(self) -> bool:
        """ Checks if given button is currently pressed.

        Returns:
           bool : True if button is pressed, false otherwise
        """
        return self._is_pressed

    def get_button_text(self) -> str:
        """ Checks given button's text and returns it.

        Returns:
           str : Button's text
        """
        return self._text

    # Setters

    def set_text(self, new_text: str) -> None:
        """Sets given button's text and updates it

        Args:
            new_text (str): Replaced text

        Raises:
            InvalidDataTypeError: Given value cannot be converted to str
        """
        try:
            str(new_text)
        except TypeError:
            raise InvalidDataTypeError(
                'Given value cannot be converted to str'
                )
        self.text = new_text
        if self.get_button_is_pressed():
            color = self.get_color('frame_active')
        else:
            color = self.get_color('frame_inactive')
        self._text_surf = self.get_font().render(new_text, True, color)
        self._set_text_pos()

    def set_button_pos(self, pos: tuple[int, int]) -> None:
        """Changes button position and automatically moves to it

        Args:
            pos (tuple[int, int]): Left x Top coordinates for object

        Raises:
            InvalidDataTypeError: Given values are not iterable
            InvalidDataLineLeghthError: Given tuple size is not equal 2
            NotANumberError: Given value is not a number
            ValueError: Given value is not greater or equal 0
        """
        self.change_frame_pos(pos)
        self._set_text_pos()
        self._original_y_pos = pos[1]

    def set_active_button_colors(self) -> None:
        """Changes given object colors to its 'active' values
        """
        self.set_text(self.get_button_text())
        self._set_bg_color(self.get_color('bg_active'))
        self._set_frame_color(self.get_color('frame_active'))

    def set_inactive_button_colors(self) -> None:
        """Changes given object colors to its 'inactive' values
        """
        self.set_text(self.get_button_text())
        self._set_bg_color(self.get_color('bg_inactive'))
        self._set_frame_color(self.get_color('frame_inactive'))

    # Private setters

    def _set_text_pos(self) -> None:
        """Sets given text position using saved coordinates
        """
        self._text_rect = self._text_surf.get_rect(
            center=self._frame_rect.center
            )


class PokemonListElem(AbstractFrame):
    def __init__(self,
                 object: GamePokemon,
                 size: tuple[float, float],
                 pos: tuple[float, float],
                 object_style: Literal[
                     'normal', 'inactive',
                     'big', 'big_inactive',
                     'no_frame', 'no_frame_inactive'] = 'no_frame'
                 ) -> None:
        """ Inits frame with given position, size, size and saves given
            GamePokemon object to itself.

        Args:
            object (GamePokemon): Saved GamePokemon object for drawing values
            size (tuple[float, float]): w x h constant size of drawable frame.
            pos (tuple[float, float]):  Left x Top position coordinates.
            object_style (str, optional): key for object style.
            Defaults to 'no_frame'.

        Raises:
            InvalidObjectTypeError: Given object is not a GamePokemon object.
            InvalidDataTypeError: Given size or pos is not a tuple or list.
            InvalidDataLineLeghthError: Given list or tuple size is not equal 2
            BadConversionError: Given float value cannot be mapped to int.
            NotANumberError: Given value is not a number.
            ValueError: Given value is not greater (or equal) 0.
            RedundantKeyError: Given object_style key does not exist.
        """

        x, y = pos

        super().__init__(size, (x + 5, y + 5), object_style)

        # Init checks
        if not isinstance(object, GamePokemon):
            raise InvalidObjectTypeError(
                'Given object is not a GamePokemon object'
                )

        # Core attributes
        self._is_pressed = False
        self._is_selected = False
        self._pokemon = object
        self._text_objects = ()
        self._set_elem_texts()
        self._current_index = 0

# Main functions

    def deselect_elem(self):
        """ Sets currently item selection value to False
        """
        self._is_selected = False

    def _set_elem_texts(self, index: int = 0) -> None:
        """Gets every single text with variables and sets tuple
        of Surface and Rect tuples: tuple[tuple[
            pygame.surface.Surface, pygame.rect.Rect]]

        Raises:
            InvalidDataTypeError: Given index type is invalid
        """

        if not isinstance(index, int):
            raise InvalidDataTypeError('Given index type is invalid')

        # Init variables

        pokemon = self.get_elem_object()
        main_color = self.get_color('font_color')
        main_font = FONTS.get('SMALLER_FONT')
        medium_font = FONTS.get('SMALL_FONT')
        x, y = self.get_pos()
        text_list = []

        # Text variables

        name_text = str(pokemon.get_name())
        name_surf = medium_font.render(
            name_text, True, main_color)
        name_rect = name_surf.get_rect(
            topleft=(x + 10, y + 8 + 60 * index))
        text_list.append((name_surf, name_rect))

        hp_text = 'HP: {}/{}'.format(
            str(pokemon.get_hp()), str(pokemon.get_max_hp())
        )
        hp_surf = medium_font.render(
            hp_text, True, main_color)
        hp_rect = hp_surf.get_rect(
            topright=(x + 380, y + 8 + 60 * index))
        text_list.append((hp_surf, hp_rect))

        stats_text = 'ATT: {}   DEF: {}   SPD: {}'.format(
            str(pokemon.get_attack()),
            str(pokemon.get_defense()),
            str(pokemon.get_speed())
        )
        stats_surf = main_font.render(
            stats_text, True, main_color)
        stats_rect = stats_surf.get_rect(
            bottomleft=(x + 10, y + 50 + 60 * index))
        text_list.append((stats_surf, stats_rect))

        types = pokemon.get_types()
        type_1 = str(types[0]).title()
        type_2 = str(types[1]).title() if types[1] else None
        types_text = str('{}, {}'.format(type_1, type_2) if type_2
                         else '{}'.format(type_1))
        types_surf = main_font.render(
            types_text, True, main_color)
        types_rect = types_surf.get_rect(
            bottomright=(x + 380, y + 50 + 60 * index))
        text_list.append((types_surf, types_rect))

        self._text_objects = tuple(text_list)

    def get_draw_values(self, index: int) -> tuple[tuple[
                tuple[int, int, int], pygame.Rect,
                tuple[int, int, int], pygame.Rect],
            tuple[tuple[pygame.surface.Surface, pygame.Rect]]
            ]:
        """ Gets every single text and frame drawing colors and
            returns if for Screen handling.

        Args:
            index (int): current index iteration for list updates

        Returns:
            tuple: tuple with 2 tuples for drawing values.
            Second tuple can contain multiple tuples with text variables.
        """
        x, y = self.get_pos()
        y = y + 60 * index
        self._frame_rect = pygame.Rect((x, y), self.get_size())
        self._bg_rect = pygame.Rect((x, y), self.get_size())

        if self.get_elem_object().get_is_alive() is False:
            self.set_object_style('no_frame_inactive')
        else:
            self.set_object_style('no_frame')

        self._set_elem_texts(index)
        self.check_click()

        return ((self._bg_color, self._bg_rect,
                self._frame_color, self._frame_rect),
                self._get_text_draw_values())

    def check_click(self):
        """Function checks if mouse is over button, if it's clicked, and if
        it's raises event for game mainloop with it's type.
        """
        self._raise_event = False
        self._event_type = None
        if self.get_object_style() == 'no_frame_inactive':
            self.set_inactive_frame_colors()
        else:
            mouse_pos = pygame.mouse.get_pos()
            if self._frame_rect.collidepoint(mouse_pos):
                if self.get_elem_is_selected():
                    self.set_active_frame_colors()
                else:
                    self.set_inactive_frame_colors()
                if pygame.mouse.get_pressed()[0]:
                    self._is_pressed = True
                elif self._is_pressed is True:
                    self._raise_event = True
                    if self.get_elem_is_selected():
                        self._event_type = 'Deselect'
                        self._is_selected = False
                        self.set_inactive_frame_colors()
                    else:
                        self._event_type = 'Select'
                        self._is_selected = True
                        self.set_active_frame_colors()
                    self._is_pressed = False

            else:
                self._is_pressed = False
                if not self.get_elem_is_selected():
                    self.set_inactive_frame_colors()

    # Getters

    def get_elem_is_pressed(self) -> bool:
        """ Checks if given element is currently pressed.

        Returns:
           bool : True if elem is pressed, false otherwise
        """
        return self._is_pressed

    def get_elem_is_selected(self) -> bool:
        """ Checks if given element is currently selected.

        Returns:
           bool : True if elem is selected, false otherwise
        """
        return self._is_selected

    def get_elem_object(self) -> GamePokemon:
        """ Checks given elements pokemon text and returns it.

        Returns:
           GamePokemon: GamePokemon object
        """
        return self._pokemon

    def get_event_type(self) -> Literal['Select', 'Deselect'] | None:
        """ Returns given event type for event handling.

        Returns:
            str | None: Object event type
        """
        return self._event_type

    # Private getters

    def _get_text_draw_values(self) -> tuple[
            tuple[pygame.surface.Surface, pygame.Rect]]:
        """Gets currently active text draw values

        Returns:
            tuple[ tuple[pygame.surface.Surface, pygame.Rect]]: All
            text rectangles and surfaces
        """
        return self._text_objects

    # Setters

    def set_elem_pos(self, pos: tuple[int, int]) -> None:
        """Changes elem position and automatically moves to it

        Args:
            pos (tuple[int, int]): Left x Top coordinates for object

        Raises:
            InvalidDataTypeError: Given values are not iterable
            InvalidDataLineLeghthError: Given tuple size is not equal 2
            NotANumberError: Given value is not a number
            ValueError: Given value is not greater or equal 0
        """
        self.change_frame_pos(pos)
        self._set_elem_texts()

    def set_active_frame_colors(self) -> None:
        """Changes given object colors to its 'active' values
        """
        self._set_bg_color(self.get_color('bg_active'))
        self._set_frame_color(self.get_color('frame_active'))

    def set_inactive_frame_colors(self) -> None:
        """Changes given object colors to its 'inactive' values
        """
        self._set_bg_color(self.get_color('bg_inactive'))
        self._set_frame_color(self.get_color('frame_inactive'))


class PokemonList(AbstractFrame):
    """ Creates empty list with ability to update it with
    PokemonListElem objects.
    """
    def __init__(self,
                 size: tuple[float, float],
                 pos: tuple[float, float],
                 object_style: Literal[
                     'normal', 'inactive',
                     'big', 'big_inactive',
                     'no_frame', 'no_frame_inactive'] = 'normal'
                 ) -> None:
        """ Initialises main list frame with given attributes and style.

        Args:
            size (tuple[float, float]): w x h constant size of drawable frame.
            pos (tuple[float, float]):  Left x Top position coordinates.
            object_style (str, optional): key for object style.
            Defaults to 'normal'.

        Raises:
            InvalidDataTypeError: Given size or pos is not a tuple or list.
            InvalidDataLineLeghthError: Given list or tuple size is not equal 2
            BadConversionError: Given float value cannot be mapped to int.
            NotANumberError: Given value is not a number.
            ValueError: Given value is not greater (or equal) 0.
            RedundantKeyError: Given object_style key does not exist.
        """

        super().__init__(size, pos, object_style)

        self._bg_color = self.get_color('bg_inactive')
        self._frame_color = self.get_color('frame_inactive')

        # Core attributes
        self._selected_elem = None
        self._elem_list = []

    # Getters

    def get_elem_list(self) -> list[PokemonListElem]:
        """ Gets private value of all saved list elements and returns it.

        Returns:
            list[PokemonListElem]: List od PokemonListElem objects.
        """
        return self._elem_list

    # Setters
    def add_elem_to_list(self, object: GamePokemon) -> None:
        """ Creates and adds PokemonListElem object using given
            GamePokemon object.\n
            Throws exception if given object is not a GamePokemon.

        Args:
            object (GamePokemon): GamePokemon object.

        Raises:
            InvalidDataTypeError: Given object is not a GamePokemon object.
        """
        if not isinstance(object, GamePokemon):
            raise InvalidDataTypeError('Given object is invalid')
        self._elem_list.append(
            PokemonListElem(object, (390, 60), self.get_pos()))

    def clear_objects(self):
        """ Clears entire list of PokemonListElem objects
        """
        self._elem_list = []

    def set_elem_list(self, pokemon_list: list[GamePokemon]) -> None:
        """ Creates and sets PokemonListElem objects using given
            list of GamePokemon objects.\n
            Throws exception if object inside list is not a GamePokemon.

        Args:
            pokemon_list (list[GamePokemon]): List with GamePokemon objects.

        Raises:
            InvalidObjectTypeError: Given object in list is not
            a GamePokemon object
        """
        elem_list = []
        for elem in pokemon_list:
            if not isinstance(elem, GamePokemon):
                raise InvalidObjectTypeError(
                    'Given object in list is not a GamePokemon object'
                    )
            elem_list.append(PokemonListElem(
                elem, (390, 60), self.get_pos()))
        self._elem_list = elem_list

    def remove_selected_object(self, selected: PokemonListElem) -> None:
        """ Removes PokemonListElem from list

        Args:
            selected (PokemonListElem): Active PokemonListElem object
        """
        for elem in self.get_elem_list():
            if elem == selected:
                self._elem_list.pop(
                    self._elem_list.index(elem)
                    )

    def set_list_pos(self, pos: tuple[int, int]) -> None:
        """Changes button position and automatically moves to it

        Args:
            pos (tuple[int, int]): Left x Top coordinates for object

        Raises:
            InvalidDataTypeError: Given values are not iterable
            InvalidDataLineLeghthError: Given tuple size is not equal 2
            NotANumberError: Given value is not a number
            ValueError: Given value is not greater or equal 0
        """
        self.change_frame_pos(pos)
        for elem in self.get_elem_list():
            elem._set_frame_pos()

    # Main functions

    def get_draw_values(self) -> tuple[tuple[
                tuple[int, int, int], pygame.Rect,
                tuple[int, int, int], pygame.Rect],
            tuple[tuple[tuple[
                tuple[int, int, int], pygame.Rect,
                tuple[int, int, int], pygame.Rect],
                tuple[pygame.surface.Surface, pygame.Rect]]]]:
        """Gets every single used value to draw pokemon list
        for Screen handling.

        Returns:
            tuple[
                tuple[
                    tuple[int, int, int], pygame.Rect,
                    tuple[int, int, int], pygame.Rect
                    ],
                tuple[
                    tuple[
                        tuple[
                            tuple[int, int, int], pygame.Rect,
                            tuple[int, int, int], pygame.Rect
                            ],
                        tuple[
                            tuple[
                                pygame.surface.Surface, pygame.Rect
                                ]
                            ]
                    ]
                ]
            ]: Tuple with given values:\n
            - First tuple: main tuple with main list frame
            - Second tuple: tuple with PokemonListFrame draw values:\n
                - First tuple: frame rectangle\n
                - Second tuple: tuples with text surf and rect objects
        """
        draw_elements = []
        for idx, elem in enumerate(self.get_elem_list()):
            draw_elements.append(elem.get_draw_values(idx))

        return ((self._bg_color, self._bg_rect,
                self._frame_color, self._frame_rect),
                tuple(draw_elements))


class SpecialListElem(AbstractFrame):
    """ Given pokemon's specials list elements for drawing.
    """
    def __init__(self,
                 pos: tuple[float, float],
                 pokemon_type: str,
                 object_style: Literal[
                     'normal', 'inactive',
                     'big', 'big_inactive',
                     'no_frame', 'no_frame_inactive'] = 'no_frame'
                 ) -> None:
        """ Initialises button with given values and style.
        Element size is constant in this object

        Args:
            pos (tuple[float, float]):  Left x Top position coordinates.
            pokemon_type (str): Given pokemon's type name
            object_style (str, optional): key for object style.
            Defaults to 'no_frame'.

        Raises:
            InvalidDataTypeError: Given size or pos is not a tuple or list,
            or given pokemon pokemon_type type is invalid.
            InvalidDataLineLeghthError: Given list or tuple size is not equal 2
            BadConversionError: Given float value cannot be mapped to int.
            NotANumberError: Given value is not a number.
            ValueError: Given value is not greater (or equal) 0.
            RedundantKeyError: Given object_style key does not exist.
        """
        if not isinstance(pokemon_type, str):
            raise InvalidDataTypeError('Given pokemon_type type is invalid.')

        x, y = pos
        size_x = 145
        size_y = 70

        super().__init__((size_x, size_y), (x + 5, y + 5), object_style)

        self._bg_color = self.get_color('bg_inactive')
        self._frame_color = self.get_color('frame_inactive')
        self._font = FONTS.get('SMALL_FONT')

        # Core attributes

        self._pokemon_type = pokemon_type
        self._is_pressed = False

    # Main functions

    def get_draw_values(self,
                        index: int = 0
                        ) -> tuple[tuple[tuple[int, int, int], pygame.Rect,
                                   tuple[int, int, int], pygame.Rect],
                                   tuple[pygame.surface.Surface, pygame.Rect]]:

        """ Gets draw walues with saved values and frames for screen handling.
            Fuction also updates colors from check_click function.

        Returns:
            tuple(tuple(tuple(int,int,int), pygame.Rect, (frame_bg)\n
                        tuple(int,int,int), pygame.Rect), (frame_frame)\n
                tuple(pygame.surface.Surface, pygame.Rect) (frame_text)
                ): tuple with 2 tuples with given object drawable values.

        """
        x, y = self.get_pos()
        x = x + index % 2 * 145
        y = y + index // 2 * 70
        self._frame_rect = pygame.Rect((x, y), self.get_size())
        self._bg_rect = pygame.Rect((x, y), self.get_size())
        text_elem = self._get_elem_texts(index)

        self.check_click()

        return ((self._bg_color, self._bg_rect,
                self._frame_color, self._frame_rect),
                text_elem)

    def check_click(self):
        """Function checks if mouse is over button, if it's clicked, and if
        it's raises event for game mainloop.
        """
        self._raise_event = False
        mouse_pos = pygame.mouse.get_pos()
        if self._frame_rect.collidepoint(mouse_pos):
            self.set_active_frame_colors()
            if pygame.mouse.get_pressed()[0]:
                self._is_pressed = True
            elif self._is_pressed is True:
                self._raise_event = True
                self._is_pressed = False
        else:
            self._is_pressed = False
            self.set_inactive_frame_colors()

    # Getters

    def get_type_text(self) -> str:
        """ Gets private value of pokemon type and returns it

        Returns:
            str: Pokemon type
        """
        return self._pokemon_type

    # Private getters

    def _get_elem_texts(self, index) -> tuple[()] | tuple[
            pygame.surface.Surface, pygame.rect.Rect]:
        """Gets every single text with variables and sets tuple
        of Surface and Rect: tuple[
            pygame.surface.Surface, pygame.rect.Rect]
        """
        # Init variables
        if not self.get_type_text():
            return ()
        main_color = self.get_color('font_color')
        main_font = FONTS.get('SMALL_FONT')
        x, y = self.get_pos()
        type_text = self.get_type_text().title()
        type_surf = main_font.render(
            type_text, True, main_color)
        type_rect = type_surf.get_rect(
            center=(x + 72 + index % 2 * 145, y + 35 + index // 2 * 70))
        return [type_surf, type_rect]

    # Setters

    def set_ability_text(self, pokemon_type: str) -> None:
        """ Sets private value of ability's name and updates it.
        Throws exception if given type is not str.

        Args:
            ability (str): Ability's name.

        Raises:
            InvalidDataTypeError: Given ability type is not string.
        """
        if not isinstance(pokemon_type, str):
            raise InvalidDataTypeError('Given ability type is not string.')
        self._pokemon_type = pokemon_type

    def set_active_frame_colors(self) -> None:
        """Changes given object colors to its 'active' values
        """
        self._set_bg_color(self.get_color('bg_active'))
        self._set_frame_color(self.get_color('frame_active'))

    def set_inactive_frame_colors(self) -> None:
        """Changes given object colors to its 'inactive' values
        """
        self._set_bg_color(self.get_color('bg_inactive'))
        self._set_frame_color(self.get_color('frame_inactive'))


class SpecialList(AbstractFrame):
    """ Special list object that can contain SpecialListElem objects
    with event handling.
    """
    def __init__(self,
                 pos: tuple[float, float],
                 object_style: Literal[
                     'normal', 'inactive',
                     'big', 'big_inactive',
                     'no_frame', 'no_frame_inactive'] = 'normal'
                 ) -> None:
        """ Initialises list with given values and style.
        Element size is constant in this object

        Args:
            pos (tuple[float, float]):  Left x Top position coordinates.
            object_style (str, optional): key for object style.
            Defaults to 'normal'.

        Raises:
            InvalidDataTypeError: Given size or pos is not a tuple or list,
            or given ability type is invalid.
            InvalidDataLineLeghthError: Given list or tuple size is not equal 2
            BadConversionError: Given float value cannot be mapped to int.
            NotANumberError: Given value is not a number.
            ValueError: Given value is not greater (or equal) 0.
            RedundantKeyError: Given object_style key does not exist.
        """
        x, y = pos
        size_x = 300
        size_y = 80

        super().__init__((size_x, size_y), (x + 5, y + 5), object_style)

        self._bg_color = self.get_color('bg_inactive')
        self._frame_color = self.get_color('frame_inactive')

        # Core attributes

        self._is_visible = False
        self._elem_list = []

    # Main functions

    def get_draw_values(self) -> tuple[tuple[
                tuple[int, int, int], pygame.Rect,
                tuple[int, int, int], pygame.Rect],
            tuple[tuple[tuple[
                tuple[int, int, int], pygame.Rect,
                tuple[int, int, int], pygame.Rect],
                tuple[pygame.surface.Surface, pygame.Rect]]]] | tuple:
        """Gets every single used value to draw pokemon list.
        If list is not visible, return one empty tuple instead.
        Function also resets event in every element in list.

        Returns:
            tuple[
                tuple[
                    tuple[int, int, int], pygame.Rect,
                    tuple[int, int, int], pygame.Rect
                    ],
                tuple[
                    tuple[
                        tuple[
                            tuple[int, int, int], pygame.Rect,
                            tuple[int, int, int], pygame.Rect
                            ],
                        tuple[
                            tuple[
                                pygame.surface.Surface, pygame.Rect
                                ]
                            ]
                    ]
                ]
            ]: Tupls with 2 tuples: main frame and tuples with list
            element objects.
        """
        for elem in self.get_elem_list():
            elem._raise_event = False
        if self.get_is_visible() is False:
            return ()
        draw_elements = []
        for idx, elem in enumerate(self.get_elem_list()):
            draw_elements.append(elem.get_draw_values(idx))

        return ((self._bg_color, self._bg_rect,
                self._frame_color, self._frame_rect),
                tuple(draw_elements))

    # Getters

    def get_is_visible(self) -> bool:
        """ Gets if given list is currnetly visible.

        Returns:
            bool: If current list visible.
        """
        return self._is_visible

    def get_elem_list(self) -> list[SpecialListElem]:
        """ Gets list with every element in list

        Returns:
            list[SpecialListElem]: list of SpecialListElem
        """
        return self._elem_list

    # Setters

    def set_is_visible(self, value: bool) -> None:
        """ Sets if given list is visible

        Args:
            value (bool): List's visiblity bool value

        Raises:
            InvalidDataTypeError: Given value is not boolean
        """
        if not isinstance(value, bool):
            raise InvalidDataTypeError('Given value is not boolean.')
        self._is_visible = value

    def set_elem_list(self, pokemon: GamePokemon) -> None:
        """Creates list with SpecialListElem objects using
        given pokemon's abilities.

        Args:
            pokemon (GamePokemon): GamePokemon object with special abilities.

        Raises:
            InvalidObjectTypeError: Given object is not GamePokemon object.
        """
        if not isinstance(pokemon, GamePokemon):
            raise InvalidObjectTypeError('Given object is not GamePokemon.')
        elem_list = []
        for elem in pokemon.get_types():
            if elem:
                elem_list.append(SpecialListElem(self.get_pos(), str(elem)))
        self._elem_list = elem_list

    def set_list_pos(self, pos: tuple[int, int]) -> None:
        """Changes button position and automatically moves to it

        Args:
            pos (tuple[int, int]): Left x Top coordinates for object

        Raises:
            InvalidDataTypeError: Given values are not iterable
            InvalidDataLineLeghthError: Given tuple size is not equal 2
            NotANumberError: Given value is not a number
            ValueError: Given value is not greater or equal 0
        """
        self.change_frame_pos(pos)
        for elem in self.get_elem_list():
            elem._set_frame_pos()


class GamePokemonList(PokemonList):
    """Special PokemonList object with ability to make it invisible.
    """
    def __init__(self,
                 size: tuple[float, float],
                 pos: tuple[float, float],
                 object_style: Literal[
                     'normal', 'inactive',
                     'big', 'big_inactive',
                     'no_frame', 'no_frame_inactive'] = 'normal'
                 ) -> None:
        """ Initialises game list with given values and style.

        Args:
            pos (tuple[float, float]):  Left x Top position coordinates.
            size (tuple[float, float]): w x h constant size of drawable frame.
            object_style (str, optional): key for object style.
            Defaults to 'normal'.

        Raises:
            InvalidDataTypeError: Given size or pos is not a tuple or list,
            or given ability type is invalid.
            InvalidDataLineLeghthError: Given list or tuple size is not equal 2
            BadConversionError: Given float value cannot be mapped to int.
            NotANumberError: Given value is not a number.
            ValueError: Given value is not greater (or equal) 0.
            RedundantKeyError: Given object_style key does not exist.
        """
        super().__init__(size, pos, object_style)

        self._is_visible = False

    # Getters

    def get_is_visible(self) -> bool:
        """ Gets if given list is currnetly visible.

        Returns:
            bool: If current list visible.
        """
        return self._is_visible

    # Setters

    def set_is_visible(self, value: bool) -> None:
        """ Sets if given list is visible

        Args:
            value (bool): List's visiblity bool value

        Raises:
            InvalidDataTypeError: Given value is not boolean
        """
        if not isinstance(value, bool):
            raise InvalidDataTypeError('Given value is not boolean.')
        self._is_visible = value

    def get_draw_values(self) -> tuple[tuple[
                tuple[int, int, int], pygame.Rect,
                tuple[int, int, int], pygame.Rect],
            tuple[tuple[tuple[
                tuple[int, int, int], pygame.Rect,
                tuple[int, int, int], pygame.Rect],
                tuple[pygame.surface.Surface, pygame.Rect]]]] | tuple:
        """Gets every single used value to draw pokemon list for
        screen handling. If it's invisible returns empty tuple instead.

        Returns:
            tuple[
                tuple[
                    tuple[int, int, int], pygame.Rect,
                    tuple[int, int, int], pygame.Rect ],
                tuple[
                    tuple[
                        tuple[
                            tuple[int, int, int], pygame.Rect,
                            tuple[int, int, int], pygame.Rect ],
                        tuple[
                            tuple[
                                pygame.surface.Surface, pygame.Rect ]
                            ]
                    ]
                ]
            ]: Tuple with given values:
            - First tuple: main tuple with main list frame
            - Second tuple: tuple with PokemonListFrame draw values:
                - First tuple: frame rectangle
                - Second tuple: tuples with text surf and rect objects
        """
        if self.get_is_visible() is True:
            return super().get_draw_values()
        else:
            return ()


class PokemonBalls(AbstractWidget):
    """ Special drawable object of how many pokeballs are active.
    """
    def __init__(self, pos: tuple[float, float]) -> None:
        """ Creates object with given coordinates and fixed size.

        Args:
            pos (tuple[float, float]): Left x Top coordinates.

        Raises:
            InvalidDataTypeError: Given value is not a tuple or list.
            InvalidDataLineLeghthError: Given list or tuple size is
            not equal 2.
            NotANumberError: Given value is not a number.
            ValueError: Given value is not greater (or equal) 0.
        """
        size_w = 400
        size_h = 60
        super().__init__((size_w, size_h), pos)

        self._small_font = FONTS.get('SMALL_FONT')
        self._big_font = FONTS.get('BIG_FONT')
        self._color = COLORS.get('LIGHT_GRAY')

    def get_draw_values(self, pokeballs_count: int) -> tuple[
        tuple[pygame.surface.Surface, pygame.Rect]
    ]:
        """Draws how many of 6 pokeballs are active.

        Args:
            pokeballs_count (int): How many pokeballs are active.

        Returns:
            tuple(tuple(pygame.surface.Surface, pygame.Rect)): Tuple with
            6 tuples containing Surface and Rect values.
        """
        if not isinstance(pokeballs_count, int):
            raise InvalidDataTypeError('Given value is not integer.')
        x, y = self.get_pos()
        text_list = []
        text = 'O'

        for pokeball_index in range(6):
            if pokeball_index < pokeballs_count:
                surf = self._big_font.render(text, True, self._color)
            else:
                surf = self._small_font.render(text, True, self._color)
            rect = surf.get_rect(
                center=(x + 50 * pokeball_index, y))

            text_list.append((surf, rect))
        return tuple(text_list)


class PokemonFrame(AbstractWidget):
    """Object for drawing currently playing pokemon.
    """
    def __init__(self, pos: tuple[float, float]) -> None:
        """Creates base frame with given position.
        Size of frame is fixed and depended of image size

        Args:
            pos (tuple[float, float]): Left x Top coordinates.

        Raises:
            InvalidDataTypeError: Given value is not a tuple or list.
            InvalidDataLineLeghthError: Given list or tuple size is
            not equal 2.
            BadConversionError: Given float value cannot be mapped to int.
            NotANumberError: Given value is not a number.
            ValueError: Given value is not greater (or equal) 0.
        """
        super().__init__((680, 174), pos)

        self._frame_img = FRAME_IMAGE
        self._active_pokemon = None

# Main functions

    def _get_draw_texts(self) -> tuple[
            tuple[int, int, int], pygame.surface.Surface
            ] | tuple[None]:
        """Gets every single text from active pokemon and returns it
            for screen handling. Returns empty tuple if it's empty.

        Returns:
            tuple(tuple(int, int, int), pygame.surface.Surface) | tuple(None):
            Tuple with tuples with text objects.
        """
        if not self.get_active_pokemon():
            return ()
        pokemon = self.get_active_pokemon()
        main_color = COLORS.get('LIGHT_GRAY')
        small_font = FONTS.get('SMALL_FONT')
        medium_font = FONTS.get('MEDIUM_FONT')
        big_font = FONTS.get('BIG_FONT')
        x, y = self.get_pos()
        text_list = []

        name_text = str(pokemon.get_name())
        name_surf = big_font.render(
            name_text, True, main_color)
        name_rect = name_surf.get_rect(
            topleft=(x + 40, y + 24))
        text_list.append((name_surf, name_rect))

        hp_text = 'HP: {}/{}'.format(
            str(pokemon.get_hp()), str(pokemon.get_max_hp())
        )
        hp_surf = medium_font.render(
            hp_text, True, main_color)
        hp_rect = hp_surf.get_rect(
            bottomright=(x + 645, y + 108))
        text_list.append((hp_surf, hp_rect))

        stats_text = 'ATT: {}   DEF: {}   SPD: {}'.format(
            str(pokemon.get_attack()),
            str(pokemon.get_defense()),
            str(pokemon.get_speed())
        )
        stats_surf = small_font.render(
            stats_text, True, main_color)
        stats_rect = stats_surf.get_rect(
            bottomleft=(x + 40, y + 146))
        text_list.append((stats_surf, stats_rect))

        types = pokemon.get_types()
        type_1 = str(types[0]).title()
        type_2 = str(types[1]).title() if types[1] else None
        types_text = str('{}, {}'.format(type_1, type_2) if type_2
                         else '{}'.format(type_1))
        types_surf = small_font.render(
            types_text, True, main_color)
        types_rect = types_surf.get_rect(
            topleft=(x + 40, y + 80))
        text_list.append((types_surf, types_rect))

        return tuple(text_list)

    def get_draw_values(self) -> tuple[tuple[
                    pygame.surface.Surface, tuple[int, int]],
                tuple[
                    tuple[int, int, int], pygame.surface.Surface]
                ]:
        """_summary_

        Returns:
            tuple(tuple(pygame.surface.Surface, tuple(int, int)),
                  tuple(tuple(int, int, int), pygame.surface.Surface)):
            Tuple with 2 tuples:
                - Tuple with image surface and position
                - Tuple with tuples with text Surface and text Rect variables.
        """
        frame_img = self._frame_img
        texts = self._get_draw_texts()
        return ((frame_img, self.get_pos()), texts)

    # Getters

    def get_active_pokemon(self) -> GamePokemon:
        """Gets private value of currently active pokemon and returns it.

        Returns:
            GamePokemon: Currently playing pokemon
        """
        return self._active_pokemon

    # Setters

    def set_active_pokemon(self, pokemon: GamePokemon) -> None:
        """ Sets active pokemon to given in argument.

        Args:
            pokemon (GamePokemon): GamePokemon object.

        Raises:
            InvalidObjectTypeError: Given object is not GamePokemon object.
        """
        if not isinstance(pokemon, GamePokemon):
            raise InvalidDataTypeError('Given value is not a GamePokemon.')
        self._active_pokemon = pokemon
