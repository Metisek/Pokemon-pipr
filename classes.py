
class MalformedPokemonDataError(ValueError):
    pass


class PokemonDataDoesNotExistError(TypeError):
    pass


class BasePokemon:
    """ Creates base pokemon for creating other pokemons from it's values
        This object is base for GamePokemon class
    """
    def __init__(self,
                 pokedex_number,
                 name,
                 abilities,
                 stats,
                 special_strength,
                 other):
        """Creates base pokemon object

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
        
        if not name:
            raise MalformedPokemonDataError('"name" does not exist')
        
        for key in special_strength:
            strength_value = special_strength[key]
            special_strength[key] = self.return_if_positive(
                self.convert_to_float(strength_value)
                )

        for key in other:
            if key != 'generation':
                other_value = other[key]
                other[key] = self.return_if_positive(
                    self.convert_to_float(other_value)
                    )
        other['generation'] = self.convert_to_int(other['generation'])

        # if len(special_strength) != 18:
        #     raise MalformedPokemonDataError('Cannot')

        self._pokedex_number = self.return_if_positive(
            self.convert_to_int(pokedex_number)
            )
        self._name = name
        self._abilities = abilities
        self._hp = self.return_if_positive(
            self.convert_to_int(stats['hp'])
            )
        self._defense = self.return_if_positive(
            self.convert_to_int(stats['defense'])
            )
        self._attack = self.return_if_positive(
            self.convert_to_int(stats['attack'])
            )
        self._type1 = stats['type1']
        self._type2 = stats['type2'] if stats['type2'] else None
        self._classfication = stats['classfication']
        self._experience_growth = self.return_if_positive(
            self.convert_to_int(stats['experience_growth'])
            )
        self._special_strength = special_strength
        self._other = other

    def convert_to_int(self, value):
        if isinstance(value, float):
            raise MalformedPokemonDataError('Given value cannot be converted to int')
        try:
            return int(value)
        except ValueError:
            raise MalformedPokemonDataError('Given value cannot be converted to int')

    def convert_to_float(self, value):
        try:
            return float(value)
        except ValueError:
            raise MalformedPokemonDataError('Given value cannot be converted to float')

    def return_if_positive(self, value):
        if value <= 0:
            raise MalformedPokemonDataError('Given value must be positive')
        return value

    def return_if_not_negative(value):
        if value < 0:
            raise MalformedPokemonDataError('Given value must not be negative')
        return value

    def get_pokedex_number(self):
        return self._pokedex_number

    def get_name(self):
        return self._name

    def get_abilities(self):
        return self._abilities

    def get_hp(self):
        return self._hp

    def set_hp(self, value):
        self._hp = self.return_if_positive(self.convert_to_int(value))

    def get_attack(self):
        return self._attack

    def set_attack(self, value):
        self._attack = self.return_if_positive(self.convert_to_int(value))

    def get_defense(self):
        return self._defense
    
    def get_types(self):
        return [self._type1, self._type2]

    def set_defense(self, value):
        self._defense = self.return_if_positive(self.convert_to_int(value))

    def get_special_strength_dict(self):
        return self._special_strength

    def get_special_strength_value(self, pokemon_type):
        dict_key = 'against_{}'.format(pokemon_type)
        try:
            return self._special_strength[dict_key]
        except KeyError:
            raise PokemonDataDoesNotExistError(
                'Given pokemon type does not exist'
            )

    def get_other_dict(self):
        return self._other

    def get_other_value(self, dict_key):
        try:
            return self._other[dict_key]
        except KeyError:
            raise PokemonDataDoesNotExistError(
                'Given data does not exist'
            )
