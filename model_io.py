import json
from classes import BasePokemon
from classes import (
    MalformedPokemonDataError,
    InvalidDataLineLeghthError,
    PokemonDataDoesNotExistError,
    NotANumberError,
    BadConversionError,
    RedundantKeyError
)
import io
from ast import literal_eval


def io_convert_to_int(value: (int | str)) -> int:
    """ Converts given string (or int) to int

    Args:
        value (int | str -> int): value convertable to int.

    Raises:
        BadConversionError: Float cannot be mapped (rounded) to int in
        this instance.
        NotANumberError: Value cannot be converted to int.

    Returns:
        int: Value as integer.
    """
    try:
        float_value = float(value)
        if float_value != int(value):
            raise BadConversionError(
                "Float cannot be mapped (rounded) to int in this instance."
                )
        return int(value)
    except ValueError:
        raise NotANumberError(
            'Given value cannot be converted to int.'
            )


def io_convert_to_float(value: (float | int | str)) -> float:
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


def io_convert_string_to_list(value: str) -> list:
    """ Converts given string to list, even if it's empty.
    Throws exception if given string cannot be interpreted as list

    Args:
        value (str -> list): list variable saved as list

    Raises:
        BadConversionError: Given string value is not convertable to list
    """
    try:
        value = literal_eval(value)
        if not isinstance(value, list):
            raise TypeError
        return value
    except ValueError:
        raise BadConversionError('Given value is not convertable to list')
    except TypeError:
        raise BadConversionError('Given string value is not a list')


def io_return_if_positive(value: (int | float)) -> (int | float):
    """ Returns value if > 0. Throws exception otherwise.

    Args:
        value (int | float): Numeric value.

    Raises:
        ValueError: Given value is not greater than 0.
        NotANumberError: Given value is not a number.

    Returns:
        int | float: Value given as argument.
    """
    if not isinstance(value, (int, float)):
        raise NotANumberError('Given value is not a number.')
    if value <= 0:
        raise ValueError('Given value must be positive.')
    return value


def io_return_if_not_negative(value: (int | float)) -> (int | float):
    """ Returns value if >= 0. Throws exception otherwise.

    Args:
        value (int | float): Numeric value.

    Raises:
        ValueError: Given value is not greater or equal 0.
        NotANumberError: Given value is not a number.

    Returns:
        int | float: Value given as argument.
    """
    if not isinstance(value, (int, float)):
        raise NotANumberError('Given value is not a number.')
    if value < 0:
        raise ValueError('Given value must be not negative.')
    return value


def io_return_if_valid_string(value: str) -> str:
    """ Returns value if string is valid (example: not empty).
    Throws exception otherwise.

    Args:
        value (string): String text.

    Raises:
        BadConversionError: Given value is not string.
        PokemonDataDoesNotExistError: Given value is empty.

    Returns:
        str: Value given as argument.
    """
    if not value:
        raise PokemonDataDoesNotExistError('Given value is empty')
    if not isinstance(value, str):
        raise BadConversionError('Given value is not string.')
    return value


def io_return_if_valid_abilities_as_list(value: str) -> list:
    """ Checks if given pokemon's abilities lit saved as string is valid.
    Throws exception if string is corrupted, returns value as list otherwise.

    Args:
        value (str): List of given pokemon's abilities saved as string

    Raises:
        PokemonDataDoesNotExistError: List or value inside list is empty
        BadConversionError: Given string value or value inside list is not
        string.

    Returns:
        list: List of given pokemon's abilities.
    """
    value = io_convert_string_to_list(io_return_if_valid_string(value))
    if not value:
        raise PokemonDataDoesNotExistError('Given list in empty')
    for item in value:
        item = io_return_if_valid_string(item)
    return value


def check_if_valid_key(key: str, keys_list: list) -> None:
    """ Checks if given key value exist in keys list.
    Throws exception if it doesn't. Returns nothing

    Args:
        key (str): key to check if exist in key_list
        keys_list (list): list with keys as str

    Raises:
        RedundantKeyError: Given key does not exist in given keys_list
    """
    if key not in keys_list:
        raise RedundantKeyError(
            'Given key: {} is invalid in given dict'.format(key)
        )


def io_return_valid_stats_dict(value: dict) -> dict:
    """ Checks if given stats dictionary is not corrupted, converts values
    to proper data type and returns it.
    Throws exception if given dict is malformed.

    Args:
        value (dict):{
                        "hp":                 int | str -> int,
                        "defense":            int | str -> int,
                        "attack":             int | str -> int,
                        "speed":              int | str -> int,
                        "type1":              str,
                        "type2":              str,
                        "classfication":      str,
                        "experience_growth":  int | str -> int
                     }

    Raises:
        ValueError: Given int or float value is not greater than 0.
        NotANumberError: Given value is not a number.
        BadConversionError: Given value cannot be converted to given data type.
        InvalidDataLineLeghthError: Number of given dict is not equal 8.
        PokemonDataDoesNotExistError: Given string value is empty
        RedundantKeyError: Given dict has invalid keys

    Returns:
        dict: Stats dictionary with converted values
    """
    stats_keys = [
                  "hp", "defense", "attack",  "speed",
                  "type1", "type2", "classfication", "experience_growth"
                 ]
    if len(value) != 8:
        raise InvalidDataLineLeghthError('Given dict size is not equal 8')
    for key in value.keys():
        check_if_valid_key(key, stats_keys)
    value['hp'] = io_return_if_positive(
        io_convert_to_int(value['hp'])
        )
    value['defense'] = io_return_if_positive(
        io_convert_to_int(value['defense'])
        )
    value['attack'] = io_return_if_positive(
        io_convert_to_int(value['attack'])
        )
    value['speed'] = io_return_if_positive(
        io_convert_to_int(value['speed'])
        )
    value['type1'] = io_return_if_valid_string(value['type1'])
    try:
        value['type2'] = io_return_if_valid_string(value['type2'])
    except PokemonDataDoesNotExistError:
        value['type2'] = None
    value['classfication'] = io_return_if_valid_string(
        value['classfication']
        )
    value['experience_growth'] = io_return_if_positive(
        io_convert_to_int(value['experience_growth'])
        )
    return value


def io_return_valid_special_strength_dict(value: dict) -> dict:
    """ Checks if given special_strength dictionary is not corrupted,
    converts values to proper data type and returns it.
    Throws exception if given dict is malformed.

    Args:
        value (dict):{
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

    Raises:
        ValueError: Given int or float value is not greater or equal 0.
        NotANumberError: Given value is not a number.
        BadConversionError: Given value cannot be converted to given data type.
        InvalidDataLineLeghthError: Number of given dict is not equal 18.
        PokemonDataDoesNotExistError: Given string value is empty
        RedundantKeyError: Given dict has invalid keys

    Returns:
        dict: Special_strength dictionary with converted values
    """
    special_stregnth_keys = [
                             "against_bug", "against_dark",
                             "against_dragon", "against_electric",
                             "against_fairy", "against_fight",
                             "against_fire", "against_flying",
                             "against_ghost", "against_grass",
                             "against_ground", "against_ice",
                             "against_normal", "against_poison",
                             "against_psychic", "against_rock",
                             "against_steel", "against_water",
                             ]
    if len(value) != 18:
        raise InvalidDataLineLeghthError('Given dict size is not equal 18')
    for key in value:
        check_if_valid_key(key, special_stregnth_keys)
        value[key] = io_return_if_not_negative(
            io_convert_to_float(value[key])
            )
    return value


def io_return_valid_other_dict(value: dict) -> dict:
    """ Checks if given other dictionary is not corrupted,
    converts values to proper data type and returns it.
    Throws exception if given dict is malformed.
    height_m and weight_kg values can mapped to None if string is empty

    Args:
        value (dict):{
                "percentage_male": float | int -> float | str -> float,
                "height_m":        float | int -> float | str -> float | None,
                "weight_kg":       float | int -> float | str -> float | None,
                "generation":      int | str -> int
                }

    Raises:
        ValueError: Given int or float value is not greater than 0.
        NotANumberError: Given value is not a number.
        BadConversionError: Given value cannot be converted to given data type.
        InvalidDataLineLeghthError: Number of given dict is not equal 4.
        PokemonDataDoesNotExistError: Given string value is empty
        RedundantKeyError: Given dict has invalid keys

    Returns:
        dict: Other dictionary with converted values
    """
    other_keys = [
                   "percentage_male", "height_m",
                   "weight_kg", "generation"
                  ]
    if len(value) != 4:
        raise InvalidDataLineLeghthError('Given dict size is not equal 4')
    for key in value:
        check_if_valid_key(key, other_keys)
    if not value["percentage_male"]:
        value["percentage_male"] = None
    else:
        value["percentage_male"] = io_return_if_not_negative(
                io_convert_to_float(value["percentage_male"])
                )
    if not value["weight_kg"]:
        value["weight_kg"] = None
    else:
        value["weight_kg"] = io_return_if_positive(
            io_convert_to_float(value["weight_kg"])
            )
    if not value["height_m"]:
        value["height_m"] = None
    else:
        value["height_m"] = io_return_if_positive(
            io_convert_to_float(value["weight_kg"])
            )
    return value


def read_from_json(file_hantle: io.TextIOWrapper) -> list:
    """ Reads every item in json file, check if it's not corrupted
    and returns list of every base pokemon if no corrupted data was found.
    Throws exception otherwise.

    Args:
        file_hantle (io.TextIOWrapper): file_hantle variable from json file.

    Raises:
        MalformedPokemonDataError: returns type of data corruption and
        row where it was found.

        Types of data corruption:
        -  BadConversionError: Given value cannot be converted to other
        datatype (example: 'test' to int or 0.5 to int).
        - PokemonDataDoesNotExistError: Important key's value is empty
        (example: 'name': '').
        - NotANumberError: Given value cannot be converted to number
        - ValueError: Given value does not meet given criteria
        (example: attack value cannot be smaller or equal 0).
        - InvalidDataLineLeghthError: Given collection size does not
        meet given criteria (example: other_dict must have 4 keys).
        - RedundantKeyError: Given key is not in given collection
        (example: stats['type3'] is prohibited).

    Returns:
        list: List of BasePokemon objects.
    """
    data = json.load(file_hantle)
    pokemon_list = []
    try:
        for idx, item in enumerate(data):
            pokedex_number = io_return_if_positive(
                io_convert_to_int(item['pokedex_number'])
                )
            name = io_return_if_valid_string(
                item['name']
                )
            abilities = io_return_if_valid_abilities_as_list(
                item['abilities']
                )
            stats = io_return_valid_stats_dict(
                item['stats']
                )
            special_strength = io_return_valid_special_strength_dict(
                item['special_strength']
                )
            other = io_return_valid_other_dict(
                item['other']
                )
            pokemon = BasePokemon(pokedex_number, name, abilities,
                                  stats, special_strength, other)
            pokemon_list.append(pokemon)
        return pokemon_list
    except BadConversionError as e:
        raise MalformedPokemonDataError(
            'Malformed non_convertable data in row {}: \n{}'.format(idx+1, e)
            )
    except PokemonDataDoesNotExistError as e:
        raise MalformedPokemonDataError(
            'Malformed empty data in row {}: \n{}'.format(idx+1, e)
            )
    except NotANumberError as e:
        raise MalformedPokemonDataError(
            'Malformed non-numeric data in row {}: \n{}'.format(idx+1, e)
            )
    except ValueError as e:
        raise MalformedPokemonDataError(
            'Malformed wrong value data in row {}: \n{}'.format(idx+1, e)
            )
    except InvalidDataLineLeghthError as e:
        raise MalformedPokemonDataError(
            'Malformed wrong data size in row {}: \n{}'.format(idx+1, e)
            )
    except RedundantKeyError as e:
        raise MalformedPokemonDataError(
            'Malformed redundant key in row {}: \n{}'.format(idx+1, e)
            )
