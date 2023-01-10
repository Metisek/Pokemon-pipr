import pygame

from classes import GamePokemon
from classes import (
    BadConversionError,
    InvalidDataTypeError,
    InvalidDataLineLeghthError,
    NotANumberError,
    RedundantKeyError

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
    def __init__(self, size: tuple[float, float],
                 pos: tuple[float, float]) -> None:
        """Initiates object using given 2 float tuples.
        Throws exception if given arguments are no

        Args:
            size (tuple[float, float]): Width x Height size in px
            pos (tuple[float, float]): Left x Top coordinates

        Raises:
            InvalidDataTypeError: Given value is not a tuple or list
            InvalidDataLineLeghthError: Given list or tuple size is not equal 2
            BadConversionError: Given float value cannot be mapped to int
            NotANumberError: Given value is not a number
            ValueError: Given value is not greater (or equal) 0
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
            raise InvalidDataTypeError('Given values are not iterable')
        except InvalidDataLineLeghthError:
            raise InvalidDataLineLeghthError('Given tuple size is not equal 2')
        except BadConversionError:
            raise BadConversionError(
                'Given float value cannot be mapped to int'
                )
        except NotANumberError:
            raise NotANumberError('Given value is not a number')
        except ValueError:
            raise ValueError(
                '''Given value is not greater (or equal) 0
                   or size variable is negative'''
                )

    # Checking functions:

    def _return_if_tuple_or_list_with_size(
            self, object: (list | tuple), size: int) -> (list | tuple):
        """_summary_

        Args:
            object (list  |  tuple): list or tuple with elements
            size (int): non-negative size of given object to check

        Raises:
            BadConversionError: Given float value cannot be mapped to int
            NotANumberError: Given size variable is not a number
            ValueError: Size of given object must not negative
            InvalidDataTypeError: Given object is not a list or tuple
            InvalidDataLineLeghthError: Given object size does not match size
            value

        Returns:
            list | tuple: object arg
        """
        try:
            size = io_return_if_not_negative(io_convert_to_int(size))
        except BadConversionError:
            raise BadConversionError(
                'Given float value cannot be mapped to int'
                )
        except NotANumberError:
            raise NotANumberError('Given size variable is not a number')
        except ValueError:
            raise ValueError('Size of given object must be not negative')
        if not isinstance(object, (tuple, list)):
            raise InvalidDataTypeError('Given values are not iterable')
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

    def raise_event(self) -> bool:
        """Returns if given object raised event, without specifying it's type

        Returns:
            _type_: _description_
        """
        return self._raise_event


class AbstractFrame(AbstractWidget):
    """Abstract frame object containing drawable rectangle with frame
    Also contains values with diffrent object modes
    """
    def __init__(self, size: tuple[float, float],
                 pos: tuple[float, float], object_style='normal') -> None:
        """_summary_

        Args:
            size (tuple[float, float]): w x h constant size of drawable frame
            pos (tuple[float, float]):  Left x Top position coordinates
            object_style (str, optional): key for object style.
            Defaults to 'normal'.

        Raises:
            InvalidDataTypeError: Given size or pos is not a tuple or list
            InvalidDataLineLeghthError: Given list or tuple size is not equal 2
            BadConversionError: Given float value cannot be mapped to int
            NotANumberError: Given value is not a number
            ValueError: Given value is not greater (or equal) 0
            RedundantKeyError: Given object_style key does not exist
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

        # Draw: Frame rectangle
        self._set_frame_pos()

        # Draw: Background rectangle
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

    def set_object_style(self, object_style: str) -> None:
        try:
            check_if_valid_key(object_style, self._colors_dict.keys())
            check_if_valid_key(object_style, self._fonts_dict.keys())
        except RedundantKeyError:
            raise RedundantKeyError('Given button type does not exist')
        self._object_style = object_style

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
    def __init__(self, text: str, size: tuple[float, float],
                 pos: tuple[float, float], object_style='normal') -> None:

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

    def _set_text_pos(self) -> None:
        """Sets given text position using saved coordinates
        """
        self._text_rect = self._text_surf.get_rect(
            center=self._frame_rect.center
            )

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

    # Main functions

    def get_draw_values(self) -> tuple[tuple[int, int, int], pygame.Rect,
                                       tuple[int, int, int], pygame.Rect,
                                       pygame.surface.Surface, pygame.Rect]:
        """_summary_

        Returns:
            tuple(
                tuple(int,int,int), pygame.Rect, (frame_bg)\n
                tuple(int,int,int), pygame.Rect, (frame_frame)\n
                pygame.surface.Surface, pygame.Rect (frame_text)
                ): tuple with given objects handled within Screen class
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

    def check_click(self):
        """Function checks if mouse is over button, if it's clicked, and if
        it's raises event for game mainloop
        """
        self._dynamic_elevation = 2
        self._raise_event = False
        if self.get_object_style() == 'inactive':
            self.set_inactive_button_colors()
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


class PokemonListElem(AbstractFrame):
    def __init__(self, object: GamePokemon,
                 pos: tuple[float, float], object_style='no_frame') -> None:

        size_x = 390
        size_y = 60
        x, y = pos

        super().__init__((size_x, size_y), (x + 5, y + 5), object_style)

        # Init checks
        if not isinstance(object, GamePokemon):
            raise InvalidDataTypeError('Given text is not a string')

        # Core attributes
        self._is_pressed = False
        self._is_selected = False
        self._pokemon = object
        self._text_objects = ()
        self._set_elem_texts()
        self._current_index = 0

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

    def _get_text_draw_values(self) -> tuple[
            tuple[pygame.surface.Surface, pygame.Rect]]:
        """Gets currently active text draw values

        Returns:
            tuple[ tuple[pygame.surface.Surface, pygame.Rect]]: All
            text rectangles and surfaces
        """
        return self._text_objects

    def get_event_type(self) -> str | None:
        return self._event_type

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

    # Main functions

    def deselect_elem(self):
        """ Sets currently item selection value
        """
        self._is_selected = False

    def _set_elem_texts(self, index=0) -> None:
        """Gets every single text with variables and sets tuple
        of Surface and Rect tuples: tuple[tuple[
            pygame.surface.Surface, pygame.rect.Rect]]
        """
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

        x, y = self.get_pos()
        y = y + 60 * index
        self._frame_rect = pygame.Rect((x, y), self.get_size())
        self._bg_rect = pygame.Rect((x, y), self.get_size())

        self._set_elem_texts(index)

        self.check_click()

        return ((self._bg_color, self._bg_rect,
                self._frame_color, self._frame_rect),
                self._get_text_draw_values())

    def check_click(self):
        """Function checks if mouse is over button, if it's clicked, and if
        it's raises event for game mainloop
        """
        self._raise_event = False
        self._event_type = None
        if self.get_object_style() == 'no_frame_inactive':
            self.set_inactive_frame_colors()
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


class PokemonList(AbstractFrame):
    def __init__(self, pos: tuple[float, float],
                 object_style='normal') -> None:

        size_x = 400
        size_y = 370

        super().__init__((size_x, size_y), pos, object_style)

        self._bg_color = self.get_color('bg_inactive')
        self._frame_color = self.get_color('frame_inactive')
        # Core attributes

        self._selected_elem = None
        self._elem_list = []

    # Getters

    def get_elem_list(self) -> list[PokemonListElem]:
        return self._elem_list

    # Setters

    def add_elem_to_list(self, object: GamePokemon) -> None:
        if not isinstance(object, GamePokemon):
            raise InvalidDataTypeError('Given object is invalid')
        self._elem_list.append(
            PokemonListElem(object, self.get_pos()))

    def remove_selected_object(self, selected: PokemonListElem) -> None:
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


class PokemonFrame(AbstractWidget):
    def __init__(self, pokemon: GamePokemon, pos: tuple[float, float]) -> None:

        super().__init__((680, 144), pos)

        self._frame_img = FRAME_IMAGE
        pass
