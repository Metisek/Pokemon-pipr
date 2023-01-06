import copy
from random import randint


class InvalidDataLineLeghthError(ValueError):
    pass


class MalformedPokemonDataError(Exception):
    pass


class PokemonDataDoesNotExistError(Exception):
    pass


class DataDoesNotExistError(Exception):
    pass


class BadConversionError(ValueError):
    pass


class RedundantKeyError(KeyError):
    pass


class NotANumberError(ValueError):
    pass


class BasePokemon:
    """ Creates base pokemon for creating other pokemons from it's values.
        Values inside this class cannot be modified.
        Non-base values that can be modified are in child class GamePokemon.
    """
    def __init__(self,
                 pokedex_number: (str | int),
                 name: str,
                 abilities: (list | tuple),
                 stats: dict,
                 special_strength: dict,
                 other: dict):
        """ Creates base pokemon object.

        Args:
            pokedex_number (int | str -> int): Positive int pokedex number.
            name (str): Name of base pokemon.
            abilities (list[*str_args]): List of usable special abilities.
            stats (
                dict{
                    "hp":                 int | str -> int,
                    "defense":            int | str -> int,
                    "attack":             int | str -> int,
                    "speed":              int | str -> int,
                    "type1":              str,
                    "type2":              str,
                    "classfication":      str,
                    "experience_growth":  int | str -> int
                }
            ): Dictionary with every single crucial base pokemon stat.
            special_strength (
                dict{
                    "against_bug":        float | int -> float | str -> float,
                    "against_dark":       float | int -> float | str -> float,
                    "against_dragon":     float | int -> float | str -> float,
                    "against_electric":   float | int -> float | str -> float,
                    "against_fairy":      float | int -> float | str -> float,
                    "against_fight":      float | int -> float | str -> float,
                    "against_fire":       float | int -> float | str -> float,
                    "against_flying":     float | int -> float | str -> float,
                    "against_ghost":      float | int -> float | str -> float,
                    "against_grass":      float | int -> float | str -> float,
                    "against_ground":     float | int -> float | str -> float,
                    "against_ice":        float | int -> float | str -> float,
                    "against_normal":     float | int -> float | str -> float,
                    "against_poison":     float | int -> float | str -> float,
                    "against_psychic":    float | int -> float | str -> float,
                    "against_rock":       float | int -> float | str -> float,
                    "against_steel":      float | int -> float | str -> float,
                    "against_water":      float | int -> float | str -> float,
                    }
                ): Strength of pokemon's special against given pokemon types.
            other (
                dict{
                    "percentage_male":    float | int -> float | str -> float,
                    "height_m":           float | int -> float | str -> float,
                    "weight_kg":          float | int -> float | str -> float,
                    "generation":         int | str -> int
                    }
                ): Bonus statistics for user's view inside game's menu.
        """
        for key in special_strength:
            strength_value = special_strength[key]
            special_strength[key] = self._return_if_not_negative(
                self._convert_to_float(strength_value)
                )
        other['percentage_male'] = self._convert_float_and_check_if_none(
            other['percentage_male'], 'non-negative'
            )
        other['height_m'] = self._convert_float_and_check_if_none(
            other['height_m'], 'positive'
            )
        other['weight_kg'] = self._convert_float_and_check_if_none(
            other['weight_kg'], 'positive'
            )
        other['generation'] = self._convert_to_int(other['generation'])
        self._pokedex_number = self._return_if_positive(
            self._convert_to_int(pokedex_number)
            )
        self._name = name
        self._abilities = tuple(abilities)
        self._base_hp = self._return_if_positive(
            self._convert_to_int(stats['hp'])
            )
        self._base_attack = self._return_if_positive(
            self._convert_to_int(stats['attack'])
            )
        self._base_defense = self._return_if_positive(
            self._convert_to_int(stats['defense'])
            )
        self._base_speed = self._return_if_positive(
            self._convert_to_int(stats['speed'])
            )
        self._type1 = stats['type1']
        self._type2 = stats['type2'] if stats['type2'] else None
        self._classfication = stats['classfication']
        self._experience_growth = self._return_if_positive(
            self._convert_to_int(stats['experience_growth'])
            )
        self._special_strength = special_strength
        self._other = other

# Private functions

    def _convert_float_and_check_if_none(
                self, value: (float | int | str | None),
                return_instance='positive'
            ) -> (float | None):
        """ Returns none if value is None.
        Checks and returns float after checking given return_instance
        Throws exception if given value is not a number or None, or if
        given float does not match return_instance (ex. 0.0 is not positive)

        Args:
            value (loat | int | str | None): Given float or None value to check

            return_instance (str, optional): Given return_instance:
            - 'positive': returns number if it's > 0.
            Throws exception otherwise.
            - 'non_negative': returns number if it's >= 0.
            Throws exception otherwise.
            - anything else: returns number if it's valid.
            Throws exception otherwise.

            Defaults to 'positive'.

        Raises:
            NotANumberError: Given non-None value cannot be converted to float
            ValueError: Given number does not match return_instance condition

        Returns:
            float | None: None type or value converted to float
        """
        if isinstance(value, type(None)):
            return value
        if return_instance == 'positive':
            value = self._return_if_positive(self._convert_to_float(value))
        elif return_instance == 'non-negative':
            value = self._return_if_not_negative(self._convert_to_float(value))
        else:
            value = self._convert_to_float(value)
        return value

    def _convert_to_int(self, value) -> int:
        """ Converts given string (or int) to int

        Args:
            value (int | str -> int): value convertable to int.

        Raises:
            BadConversionError: Float cannot be mapped (rounded) to int in
            this object.
            NotANumberError: Value cannot be converted to int.

        Returns:
            int: Value as integer.
        """
        try:
            float_value = float(value)
        except ValueError:
            raise NotANumberError(
                'Given value cannot be converted to int.'
                )
        if float_value != int(value):
            raise BadConversionError(
                "Float cannot be mapped (rounded) to int in this instance."
            )
        return int(value)

    def _convert_to_float(self, value) -> float:
        """ Converts given string, int or float to float

        Args:
            value (float | int -> float | str -> float): value
            convertable to float.

        Raises:
            NotANumberError: Value cannot be converted to float.

        Returns:
            float: Value as float.
        """
        try:
            return float(value)
        except ValueError:
            raise NotANumberError(
                'Given value cannot be converted to float.'
                )

    def _return_if_positive(self, value):
        """ Returns value if > 0. Throws exception otherwise.

        Args:
            value (int | float): Numeric value.

        Raises:
            ValueError: Given value is not greater than 0.
            NotANumberError: Given value is not a number.

        Returns:
            int | float: Value given as argument.
        """
        if not isinstance(value, (int | float)):
            raise NotANumberError('Given value is not a number.')
        if value <= 0:
            raise ValueError('Given value must be positive.')
        return value

    def _return_if_not_negative(self, value):
        """ Returns value if it's greater or equal 0.
        Throws exception otherwise.

        Args:
            value (int | float): Numeric value.

        Raises:
            ValueError: Given value is not greater or equal 0.
            NotANumberError: Given value is not a number.

        Returns:
            type(value): Value given as argument.
        """
        if not isinstance(value, (int | float)):
            raise NotANumberError('Given value is not a number.')
        if value < 0:
            raise ValueError('Given value must not be negative.')
        return value

# Getters

    def get_pokedex_number(self) -> int:
        """ Gets private value of pokemon's pokedex number and returns it.

        Returns:
           int : Value of pokemon's pokedex number.
        """
        return self._pokedex_number

    def get_name(self) -> str:
        """ Gets private value of pokemon's name and returns it.

        Returns:
           str : Pokemon's name.
        """
        return self._name

    def get_abilities(self) -> tuple:
        """ Gets private value with pokemon's abilities tuple and returns it.

        Returns:
           (*str_args) : Tuple with string values.
        """
        return self._abilities

    def get_base_hp(self) -> int:
        """ Gets private value of pokemon's base HP and returns it.

        Returns:
           int : Value of pokemon's base HP.
        """
        return self._base_hp

    def get_base_attack(self) -> int:
        """ Gets private value of pokemon's base attack and returns it.

        Returns:
           int : Value of pokemon's base attack.
        """
        return self._base_attack

    def get_base_defense(self) -> int:
        """ Gets private value of pokemon's base attack and returns it.

        Returns:
           int : Value of pokemon's base defense.
        """
        return self._base_defense

    def get_base_speed(self) -> int:
        """ Gets private value of pokemon's base speed and returns it.

        Returns:
           int : Value of pokemon's base speed.
        """
        return self._base_speed

    def get_types(self) -> tuple:
        """ Gets both private pokemon types inside tuple and returns it.
        Second type can be None instead of string value if it doesn't exist.

        Returns:
            tuple(str, str | None): Tuple with one or two pokemon types.
        """
        return (self._type1, self._type2)

    def get_special_strength_dict(self) -> dict:
        """ Gets entire pokemon's special strength dictionary and returns it.

        Returns: dict{
                    "against_bug":        float
                    "against_dark":       float
                    "against_dragon":     float
                    "against_electric":   float
                    "against_fairy":      float
                    "against_fight":      float
                    "against_fire":       float
                    "against_flying":     float
                    "against_ghost":      float
                    "against_grass":      float
                    "against_ground":     float
                    "against_ice":        float
                    "against_normal":     float
                    "against_poison":     float
                    "against_psychic":    float
                    "against_rock":       float
                    "against_steel":      float
                    "against_water":      float
                 }: Dictionary with strength against every single pokemon type.
        """
        return self._special_strength

    def get_special_strength_value(self, pokemon_type) -> float:
        """ Gets specific pokemon's special stregth using other pokemon's type.
        Returns it if type exist, otherwise throws exception.

        Args:
            pokemon_type (str): Type of enemy pokemon.

        Raises:
            PokemonDataDoesNotExistError: Given pokemon type does not exist.

        Returns:
            float: Value of special strength against given pokemon type.
        """
        dict_key = 'against_{}'.format(pokemon_type)
        try:
            return self._special_strength[dict_key]
        except KeyError:
            raise PokemonDataDoesNotExistError(
                'Given pokemon type does not exist'
            )

    def get_other_dict(self) -> dict:
        """ Gets entire pokemon's other values dictionary and returns it.

        Returns: dict{
                    "percentage_male":   float
                    "height_m":          float
                    "weight_kg":         float
                    "generation":        int
                 }: Dictionary with other pokemon values.
        """
        return self._other

    def get_other_value(self, other_dict_key) -> (int | float | None):
        """ Gets specific pokemon's value from other dictionary with given arg.
        Returns it if type exist, otherwise throws exception.

        Args:
            other_dict_key (str): Key for other dict.

        Raises:
            PokemonDataDoesNotExistError: Given key does not exist in other.

        Returns:
            int | float | None: Value of given dictionary's key.
        """
        try:
            return self._other[other_dict_key]
        except KeyError:
            raise PokemonDataDoesNotExistError(
                'Given key does not exist'
            )


class GamePokemon(BasePokemon):
    """ Creates game pokemon with every needed method to make it playable.
        Values not inherited from BasePokemon can be set or modified in game.
    """
    def __init__(self, base_pokemon: BasePokemon, randomize=True):
        """ Creates playable pokemon character that inherits values
        from BasePokemon class and randomizes some if needed.

        Args:
            base_pokemon (BasePokemon): Base pokemon for values inheitance.
            randomize (bool, optional): Makes random values from other dict.
            Keeps then at default if set to false.
            If false, gender is based on "percentage_male" value.
            If greater than 50, sets to Male. Sets to female otherwise.
            If value is None type, sets to unknown instead
            Defaults to True.
        """
        self.__dict__ = copy.deepcopy(base_pokemon.__dict__)
        self._max_hp = self.get_base_hp()
        self._hp = self.get_base_hp()
        self._attack = self.get_base_attack()
        self._defense = self.get_base_defense()
        self._speed = self.get_base_speed()
        self._is_alive = True
        if randomize:
            if not isinstance(
                        self.get_other_value('percentage_male'), type(None)
                    ):
                if randint(1, 99) > self.get_other_value('percentage_male'):
                    self._gender = 'Male'
                else:
                    self._gender = 'Female'
            else:
                self._gender = 'Unknown'

            self._weight_kg = self.get_other_value('weight_kg')
            if not isinstance(self.get_weight(), type(None)):
                self._weight_kg = self._randomize_and_round_float(
                        self.get_weight(),
                    )
            self._height_m = self.get_other_value('height_m')
            if not isinstance(self.get_height(), type(None)):
                self._height_m = self._randomize_and_round_float(
                        self.get_height(),
                    )
        else:
            if not isinstance(
                self.get_other_value('percentage_male'), type(None)
            ):
                self._gender = str(
                    'Male' if self.get_other_value('percentage_male') > 50
                    else 'Female'
                )
            else:
                self._gender = 'Unknown'
            self._height_m = self.get_other_value('height_m')
            self._weight_kg = self.get_other_value('weight_kg')

# Private functions

    def _randomize_and_round_float(self, number: (float),
                                   min_range=80, max_range=120) -> float:

        """ Randomizes and return float rounded to first digit after period.
        Given min_range and max_range values are base percentage of
        which given number should be scaled.

        Args:
            number (float): number to randomize
            min_range (int | optional): minimum random range
            in percentage. Defaults to 80(%).
            max_range (int | optional): maximum random range
            in percentage. Defaults to 120(%).

        Raises:
            ValueError: Given minimum range value is greater or equal
            to maximum range value.

        Returns:
            float: Randomized and rounded float.
        """
        if min_range >= max_range:
            raise ValueError(
                'Given range minimum value is greater or equal maximum.'
                )
        random_percent = randint(min_range, max_range)
        number = round(number * random_percent / 100, 1)
        return number

# Getters

    def get_max_hp(self) -> int:
        """ Gets private value of pokemon's max_hp and returns it.

        Returns:
           int : Value of pokemon's max_hp.
        """
        return self._max_hp

    def get_hp(self) -> int:
        """ Gets private value of pokemon's hp and returns it.

        Returns:
           int : Value of pokemon's max_hp.
        """
        return self._hp

    def get_attack(self) -> int:
        """ Gets private value of pokemon's attack and returns it.

        Returns:
           int : Value of pokemon's attack.
        """
        return self._attack

    def get_defense(self) -> int:
        """ Gets private value of pokemon's defense and returns it.

        Returns:
           int : Value of pokemon's defense.
        """
        return self._defense

    def get_speed(self) -> int:
        """ Gets private value of pokemon's speed and returns it.

        Returns:
           int : Value of pokemon's speed.
        """
        return self._speed

    def get_gender(self) -> str:
        """ Gets private value of pokemon's gender and returns it.

        Returns:
           str : Pokemon's gender ("Male" or "Female").
        """
        return self._gender

    def get_height(self) -> float:
        """ Gets private value of pokemon's height and returns it.

        Returns:
           float : Value of pokemon's height (in meters).
        """
        return self._height_m

    def get_weight(self) -> float:
        """ Gets private value of pokemon's weight and returns it.

        Returns:
           float : Value of pokemon's height (in kilograms).
        """
        return self._weight_kg

    def get_is_alive(self) -> bool:
        """ Checks if pokemon is alive and returns it's state.

        Returns:
           bool : Is pokemon alive.
        """
        return self._is_alive

# Private setters

    def _set_is_alive(self, value: bool) -> None:
        """ Sets if pokemon is alive (it's HP must be greater than 0).
        Cannot be called by itself, only via other function, like set_hp.

        Args:
            value (bool): Is pokemon alive

        Raises:
            MalformedPokemonDataError: Given value is not boolean
        """
        if not isinstance(value, bool):
            raise MalformedPokemonDataError('Given value is not boolean')
        self._is_alive = value

# Setters

    def set_max_hp(self, value: int) -> None:
        """ Sets value of pokemon's max_hp if it's greater than zero.
        Throws exception otherwise.
        If current hp value in greater than new max_hp, function also
        sets hp value to max_hp.

        Args:
            value (int): Positive integer for setting private max_hp value.

        Raises:
            BadConversionError: Float cannot be mapped (rounded) to int in
            this object.
            NotANumberError: Value cannot be converted to int.
            ValueError: Given value is not greater than 0.
        """
        value = self._return_if_positive(self._convert_to_int(value))
        self._max_hp = value
        if value < self.get_hp():
            self.set_hp(value)

    def set_hp(self, value: int) -> None:
        """Sets value of pokemon's hp if it's greater or equal zero.
        Throws exception otherwise.

        Args:
            value (int): Non_negative integer for setting private hp value.

        Raises:
            BadConversionError: Float cannot be mapped (rounded) to int in
            this object.
            NotANumberError: Value cannot be converted to int.
            ValueError: Given value is not greater or equal 0.
        """
        value = self._return_if_not_negative(self._convert_to_int(value))
        self._hp = value
        if value == 0:
            self._set_is_alive(False)
        else:
            self._set_is_alive(True)

    def set_attack(self, value: int) -> None:
        """ Sets value of pokemon's attack if it's greater or equal zero.
        Throws exception otherwise.

        Args:
            value (int): Non-negative integer for setting private attack value.

        Raises:
            BadConversionError: Float cannot be mapped (rounded) to int in
            this object.
            NotANumberError: Value cannot be converted to int.
            ValueError: Given value is not greater or equal 0.
        """
        value = self._return_if_not_negative(self._convert_to_int(value))
        self._attack = value

    def set_defense(self, value: int) -> None:
        """ Sets value of pokemon's defense if it's greater than zero.
        Throws exception otherwise.

        Args:
            value (int): Positive integer for setting private defense value.

        Raises:
            BadConversionError: Float cannot be mapped (rounded) to int in
            this object.
            NotANumberError: Value cannot be converted to int.
            ValueError: Given value is not greater than 0.
        """
        value = self._return_if_positive(self._convert_to_int(value))
        self._defense = value
