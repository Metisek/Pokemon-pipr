
class MalformedPokemonDataError(ValueError):
    pass


class PokemonDataDoesNotExistError(TypeError):
    pass


class BadConversionError(ValueError):
    pass


class NotANumberError(ValueError):
    pass


class BasePokemon:
    """ Creates base pokemon for creating other pokemons from it's values
        Values inside this class cannot be modified.
        Non-base values that can be modified are in child class GamePokemon
    """
    def __init__(self,
                 pokedex_number,
                 name,
                 abilities,
                 stats,
                 special_strength,
                 other):
        """ Creates base pokemon object

        Args:
            pokedex_number (int, str -> int): Positive int pokedex number

            name (str): Name of base pokemon

            abilities (list[*str_args]): List of usable special abilities

            stats (
                dict{
                    "hp":                   int, str -> int,
                    "defense":              int, str -> int,
                    "attack":               int, str -> int,
                    "speed":                int, str -> int,
                    "type1":                str,
                    "type2":                str,
                    "classfication":        str,
                    "experience_growth":    int, str -> int
                }
            ): Dictionary with every single crucial base pokemon stat

            special_strength (
                dict{
                    "against_bug":          float, int -> float, str -> float,
                    "against_dark":         float, int -> float, str -> float,
                    "against_dragon":       float, int -> float, str -> float,
                    "against_electric":     float, int -> float, str -> float,
                    "against_fairy":        float, int -> float, str -> float,
                    "against_fight":        float, int -> float, str -> float,
                    "against_fire":         float, int -> float, str -> float,
                    "against_flying":       float, int -> float, str -> float,
                    "against_ghost":        float, int -> float, str -> float,
                    "against_grass":        float, int -> float, str -> float,
                    "against_ground":       float, int -> float, str -> float,
                    "against_ice":          float, int -> float, str -> float,
                    "against_normal":       float, int -> float, str -> float,
                    "against_poison":       float, int -> float, str -> float,
                    "against_psychic":      float, int -> float, str -> float,
                    "against_rock":         float, int -> float, str -> float,
                    "against_steel":        float, int -> float, str -> float,
                    "against_water":        float, int -> float, str -> float,
                    }
                ): Strength of pokemon's special against specific pokemon types
            other (
                dict{
                    "percentage_male":      float, int -> float, str -> float,
                    "height_m":             float, int -> float, str -> float,
                    "weight_kg":            float, int -> float, str -> float,
                    "generation":           int, str -> int
                    }
                ): Bonus statistics for user's view inside game's menu
        """
        for key in special_strength:
            strength_value = special_strength[key]
            special_strength[key] = self._return_if_positive(
                self._convert_to_float(strength_value)
                )
        for key in other:
            if key != 'generation':
                other_value = other[key]
                other[key] = self._return_if_positive(
                    self._convert_to_float(other_value)
                    )
        other['generation'] = self._convert_to_int(other['generation'])
        self._pokedex_number = self._return_if_positive(
            self._convert_to_int(pokedex_number)
            )
        self._name = name
        self._abilities = abilities
        self._base_hp = self._return_if_positive(
            self._convert_to_int(stats['hp'])
            )
        self._base_defense = self._return_if_positive(
            self._convert_to_int(stats['defense'])
            )
        self._base_attack = self._return_if_positive(
            self._convert_to_int(stats['attack'])
            )
        self._type1 = stats['type1']
        self._type2 = stats['type2'] if stats['type2'] else None
        self._classfication = stats['classfication']
        self._experience_growth = self._return_if_positive(
            self._convert_to_int(stats['experience_growth'])
            )
        self._special_strength = special_strength
        self._other = other

    def _convert_to_int(self, value):
        """ Converts given string (or int) to int

        Args:
            value (int, str -> int): value convertable to int

        Raises:
            BadConversionError: Float cannot be mapped (rounded) to int
            MalformedPokemonDataError: Value cannot be converted to int

        Returns:
            int: Value as integer
        """
        if isinstance(value, float):
            raise BadConversionError(
                'Float cannot be mapped to int in this object'
                )
        try:
            return int(value)
        except ValueError:
            raise NotANumberError(
                'Given value cannot be converted to int'
                )

    def _convert_to_float(self, value):
        """ Converts given string, int or float to float

        Args:
            value (float, int -> float, str -> float): value float-convertable

        Raises:
            MalformedPokemonDataError: Value cannot be converted to float

        Returns:
            float: Value as float
        """
        try:
            return float(value)
        except ValueError:
            raise NotANumberError(
                'Given value cannot be converted to float'
                )

    def _return_if_positive(self, value):
        """ Returns value if > 0. Throws exception otherwise

        Args:
            value (int, float): Numeric value

        Raises:
            ValueError: Given value is not greater than 0
            NotANumberError: Given value is not a number

        Returns:
            type(value): Value given as argument
        """
        if not isinstance(value, (int, float)):
            raise NotANumberError('Given value is not a number')
        if value <= 0:
            raise ValueError('Given value must be positive')
        return value

    def _return_if_not_negative(value):
        """ Returns value if  => 0. Throws exception otherwise

        Args:
            value (int, float): Numeric value

        Raises:
            ValueError: Given value is not greater or equal 0
            NotANumberError: Given value is not a number

        Returns:
            type(value): Value given as argument
        """
        if not isinstance(value, (int, float)):
            raise NotANumberError('Given value is not a number')
        if value < 0:
            raise ValueError('Given value must not be negative')
        return value

    def get_pokedex_number(self):
        """ Gets private value of pokedex number and returns it

        Returns:
           int : Value of pokedex number
        """
        return self._pokedex_number

    def get_name(self):
        """ Gets private value of name and returns it

        Returns:
           str : Value of name
        """
        return self._name

    def get_abilities(self):
        """ Gets private value with abilities list with strings and returns it

        Returns:
           [*str_args] : List with string values
        """
        return self._abilities

    def get_base_hp(self):
        """ Gets private value of pokemon's base HP and returns it

        Returns:
           int : Value of pokemon's base HP
        """
        return self._base_hp

    def get_base_attack(self):
        """ Gets private value of pokemon's base attack and returns it

        Returns:
           int : Value of pokemon's base attack
        """
        return self._base_attack

    def get_base_defense(self):
        """ Gets private value of pokemon's base attack and returns it

        Returns:
           int : Value of pokemon's base defense
        """
        return self._defense

    def get_types(self):
        """ Gets both private pokemon types inside tuple and returns it
        Second type can be None instead of string value if it doesn't exist
        
        Returns:
            tuple(str, str or None): Tuple with one or two pokemon types
        """
        return (self._type1, self._type2)

    def get_special_strength_dict(self):
        """ Gets entire pokemon's special strength dictionary and returns it

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
                 }: Dictionary with strength against every single pokemon type
        """
        return self._special_strength

    def get_special_strength_value(self, pokemon_type):
        """ Gets specific pokemon's special stregth using other pokemon's type
        Returns it if type exist, otherwise throws exception

        Args:
            pokemon_type (str): Type of enemy pokemon

        Raises:
            PokemonDataDoesNotExistError: Given pokemon type does not exist

        Returns:
            float: Value of special strength against given pokemon type
        """
        dict_key = 'against_{}'.format(pokemon_type)
        try:
            return self._special_strength[dict_key]
        except KeyError:
            raise PokemonDataDoesNotExistError(
                'Given pokemon type does not exist'
            )

    def get_other_dict(self):
        """ Gets entire pokemon's other values dictionary and returns it

        Returns: dict{
                    "percentage_male":   float
                    "height_m":          float
                    "weight_kg":         float
                    "generation":        int
                 }: Dictionary with other pokemon values
        """
        return self._other

    def get_other_value(self, other_dict_key):
        """ Gets specific pokemon's value from other dictionary with given arg
        Returns it if type exist, otherwise throws exception

        Args:
            other_dict_key (str): Key for other dict

        Raises:
            PokemonDataDoesNotExistError: Given key does not exist in other

        Returns:
            float or int: Value of given dictionary's key
        """
        try:
            return self._other[other_dict_key]
        except KeyError:
            raise PokemonDataDoesNotExistError(
                'Given key does not exist'
            )
