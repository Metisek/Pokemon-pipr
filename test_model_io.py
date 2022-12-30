from model_io import (
    read_from_json,
    io_return_if_valid_string,
    io_return_if_positive,
    io_return_if_not_negative,
    io_return_if_valid_abilities_as_list,
    io_return_valid_stats_dict,
    io_return_valid_special_strength_dict
)
from classes import (
    # MalformedPokemonDataError,
    InvalidDataLineLeghthError,
    PokemonDataDoesNotExistError,
    NotANumberError,
    BadConversionError,
    RedundantKeyError
)
from io import StringIO
# from classes import BasePokemon
import copy
from pytest import raises

global test_database
global fake_database
global test_stats
global fake_stats
global test_special_strength
global fake_special_strength
global test_other
global fake_other

test_database = """[
            {
                "pokedex_number": "1",
                "name": "Bulbasaur",
                "abilities": "['Overgrow', 'Chlorophyll']",
                "stats": {
                    "hp": "45",
                    "defense": "49",
                    "attack": "49",
                    "speed": "45",
                    "type1": "grass",
                    "type2": "poison",
                    "classfication": "Seed Pokémon",
                    "experience_growth": "1059860"
                },
                "special_strength": {
                    "against_bug": "1",
                    "against_dark": "1",
                    "against_dragon": "1",
                    "against_electric": "0.5",
                    "against_fairy": "0.5",
                    "against_fight": "0.5",
                    "against_fire": "2",
                    "against_flying": "2",
                    "against_ghost": "1",
                    "against_grass": "0.25",
                    "against_ground": "1",
                    "against_ice": "2",
                    "against_normal": "1",
                    "against_poison": "1",
                    "against_psychic": "2",
                    "against_rock": "1",
                    "against_steel": "1",
                    "against_water": "0.5"
                },
                "other": {
                    "percentage_male": "88.1",
                    "height_m": "0.7",
                    "weight_kg": "6.9",
                    "generation": "1"
                }
            }
        ]"""

test_stats = {
    "hp": "45",
    "defense": "49",
    "attack": "49",
    "speed": "45",
    "type1": "grass",
    "type2": "poison",
    "classfication": "Seed Pokémon",
    "experience_growth": "1059860"
}
test_special_strength = {
    "against_bug": "1",
    "against_dark": "1",
    "against_dragon": "1",
    "against_electric": "0.5",
    "against_fairy": "0.5",
    "against_fight": "0.5",
    "against_fire": "2",
    "against_flying": "2",
    "against_ghost": "1",
    "against_grass": "0.25",
    "against_ground": "1",
    "against_ice": "2",
    "against_normal": "1",
    "against_poison": "1",
    "against_psychic": "2",
    "against_rock": "1",
    "against_steel": "1",
    "against_water": "0.5"
}
test_other = {
    "percentage_male": "88.1",
    "height_m": "0.7",
    "weight_kg": "6.9",
    "generation": "1"
}
fake_database = []
fake_stats = {}
fake_special_strengt = {}
fake_other = {}


def test_model_io_return_if_valid_string_typical():
    io_return_if_valid_string('Labolatorium')


def test_model_io_return_if_valid_string_empty():
    with raises(PokemonDataDoesNotExistError):
        io_return_if_valid_string('')


def test_model_io_return_if_valid_string_wrong_datatype():
    with raises(BadConversionError):
        io_return_if_valid_string(22)


def test_model_io_return_if_positive_typical():
    io_return_if_positive(22)


def test_model_io_return_if_positive_float():
    io_return_if_positive(44.4)


def test_model_io_return_if_positive_zero():
    with raises(ValueError):
        io_return_if_positive(0)


def test_model_io_return_if_positive_negative():
    with raises(ValueError):
        io_return_if_positive(-5)


def test_model_io_return_if_positive_wrong_datatype():
    with raises(NotANumberError):
        io_return_if_positive("test")


def test_model_io_return_if_not_negative_typical():
    io_return_if_not_negative(22)


def test_model_io_return_if_not_negative_float():
    io_return_if_not_negative(44.4)


def test_model_io_return_if_not_negative_zero():
    io_return_if_not_negative(0)


def test_model_io_return_if_not_negative_negative():
    with raises(ValueError):
        io_return_if_not_negative(-5)


def test_model_io_return_if_not_negative_wrong_datatype():
    with raises(NotANumberError):
        io_return_if_positive("test")


def test_model_io_return_if_valid_abilities_as_list_typical():
    abilities_list = "['Special_1', 'Special_2']"
    io_return_if_valid_abilities_as_list(abilities_list)


def test_model_io_return_if_valid_abilities_as_list_empty_list():
    abilities_list = "[]"
    with raises(PokemonDataDoesNotExistError):
        io_return_if_valid_abilities_as_list(abilities_list)


def test_model_io_return_if_valid_abilities_as_list_empty_string():
    abilities_list = ""
    with raises(PokemonDataDoesNotExistError):
        io_return_if_valid_abilities_as_list(abilities_list)


def test_model_io_return_if_valid_abilities_as_list_invalid_value():
    abilities_list = 22
    with raises(BadConversionError):
        io_return_if_valid_abilities_as_list(abilities_list)


def test_model_io_return_if_valid_abilities_as_list_invalid_values_in_list():
    abilities_list = "['Special_1', 22]"
    with raises(BadConversionError):
        io_return_if_valid_abilities_as_list(abilities_list)


def test_model_io_return_valid_stats_dict_typical():
    stats_dict = io_return_valid_stats_dict(test_stats)
    assert stats_dict['hp'] == 45
    assert stats_dict['attack'] == 49
    assert stats_dict['defense'] == 49
    assert stats_dict['speed'] == 45
    assert stats_dict['type1'] == 'grass'
    assert stats_dict['type2'] == 'poison'
    assert stats_dict['classfication'] == 'Seed Pokémon'
    assert stats_dict['experience_growth'] == 1059860


def test_model_io_return_valid_stats_dict_int_as_str():
    fake_stats = copy.deepcopy(test_stats)
    fake_stats['hp'] = 'test'
    with raises(NotANumberError):
        io_return_valid_stats_dict(fake_stats)


def test_model_io_return_valid_stats_dict_str_as_int():
    fake_stats = copy.deepcopy(test_stats)
    fake_stats['type1'] = 22
    with raises(BadConversionError):
        io_return_valid_stats_dict(fake_stats)


def test_model_io_return_valid_stats_dict_empty_str():
    fake_stats = copy.deepcopy(test_stats)
    fake_stats['type1'] = ''
    with raises(PokemonDataDoesNotExistError):
        io_return_valid_stats_dict(fake_stats)


def test_model_io_return_valid_stats_dict_invalid_keys_count():
    fake_stats = copy.deepcopy(test_stats)
    fake_stats['type3'] = 'Test ability'
    with raises(InvalidDataLineLeghthError):
        io_return_valid_stats_dict(fake_stats)


def test_model_io_return_valid_stats_dict_wrong_keys():
    fake_stats = copy.deepcopy(test_stats)
    fake_stats.pop('hp')
    fake_stats['type3'] = 'Test ability'
    with raises(RedundantKeyError):
        io_return_valid_stats_dict(fake_stats)


def test_model_io_return_valid_special_strength_dict_typical():
    special_strength_dict = io_return_valid_special_strength_dict(
        test_special_strength
        )
    assert special_strength_dict['against_bug'] == 1


def test_model_io_return_valid_special_strength_dict_float_as_str():
    fake_special_strength = copy.deepcopy(test_special_strength)
    fake_special_strength['against_bug'] = 'test'
    with raises(NotANumberError):
        io_return_valid_special_strength_dict(fake_special_strength)


def test_model_io_return_valid_special_strength_dict_empty_value():
    fake_special_strength = copy.deepcopy(test_special_strength)
    fake_special_strength['against_bug'] = ''
    with raises(NotANumberError):
        io_return_valid_special_strength_dict(fake_special_strength)


def test_model_io_return_valid_special_strength_dict_invalid_keys_count():
    fake_special_strength = copy.deepcopy(test_special_strength)
    fake_special_strength['pipr_jest_spoko'] = '0.25'
    with raises(InvalidDataLineLeghthError):
        io_return_valid_special_strength_dict(fake_special_strength)


def test_model_io_return_valid_special_strength_dict_wrong_keys():
    fake_special_strength = copy.deepcopy(test_special_strength)
    fake_special_strength.pop('against_bug')
    fake_special_strength['pipr_jest_spoko'] = '0.25'
    with raises(RedundantKeyError):
        io_return_valid_special_strength_dict(fake_special_strength)


def test_model_io_read_from_json_test_database():
    file_hantle = StringIO(str(test_database))
    data = read_from_json(file_hantle)
    file_hantle.close()
    assert data[0].get_base_hp() == 45


def test_model_io_read_from_json_check_full_data():
    file_hantle = open('pokemon.json', 'r')
    data = read_from_json(file_hantle)
    file_hantle.close()
    assert len(data) == 801
    assert data[0].get_base_hp() == 45
    assert data[799].get_name() == 'Necrozma'
