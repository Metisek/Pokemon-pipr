from database import PokemonDatabase
from pytest import raises
from classes import (
    BadConversionError,
    PokemonDataDoesNotExistError,
    DataDoesNotExistError,
    NotANumberError
)


def load_correct_database():
    path = 'pokemon.json'
    database = PokemonDatabase(path)
    return database


def test_database_init_typical():
    path = 'pokemon.json'
    database = PokemonDatabase(path)
    assert len(database.get_pokemon_database_list()) > 800
    assert database._get_base_file_path() == 'pokemon.json'


def test_database_load_from_json_typical():
    path = 'pokemon.json'
    database = PokemonDatabase(path)
    data = database.get_pokemon_database_list()
    assert data[0].get_base_hp() == 45


def test_database_load_from_json_file_not_found():
    path = 'DefinitywnieTenPlikNieIstnieje.json'
    with raises(FileNotFoundError):
        PokemonDatabase(path)


def test_database_load_from_json_path_is_a_directory():
    path = 'reference'
    with raises(IsADirectoryError):
        PokemonDatabase(path)


def test_database_search_name_typical():
    database = load_correct_database()
    substring = 'Cha'
    search_result = database._search_name(substring)
    assert len(search_result) == 13
    assert search_result[0].get_name() == 'Charmander'
    assert search_result[5].get_name() == 'Chansey'


def test_database_search_name_empty_text():
    database = load_correct_database()
    substring = ''
    search_result = database._search_name(substring)
    assert len(search_result) == 0


def test_database_search_name_no_find():
    database = load_correct_database()
    substring = 'testowanko'
    search_result = database._search_name(substring)
    assert len(search_result) == 0


def test_database_search_pokedex_number_typical():
    database = load_correct_database()
    number = 56
    search_result = database._search_pokedex_number(number)
    assert len(search_result) == 18
    assert search_result[0].get_pokedex_number() == 56
    assert search_result[1].get_pokedex_number() == 156


def test_database_search_pokedex_number_zero():
    database = load_correct_database()
    number = 0
    search_result = database._search_pokedex_number(number)
    assert len(search_result) == 0


def test_database_search_pokedex_number_large_number():
    database = load_correct_database()
    number = 799
    search_result = database._search_pokedex_number(number)
    assert len(search_result) == 1


def test_database_search_pokedex_number_very_large_number():
    database = load_correct_database()
    number = 79900
    search_result = database._search_pokedex_number(number)
    assert len(search_result) == 0


def test_database_search_database_string_typical():
    database = load_correct_database()
    substring = "Pik"
    search_result = database.search_database(substring)
    assert len(search_result) == 2
    assert search_result[0].get_name() == 'Pikachu'


def test_database_search_database_string_not_existing_pokemon():
    database = load_correct_database()
    substring = "PikaPikaPikaPika"
    search_result = database.search_database(substring)
    assert isinstance(search_result, type(None))


def test_database_search_database_string_empty():
    database = load_correct_database()
    substring = ""
    search_result = database.search_database(substring)
    assert len(search_result) > 100


def test_database_search_database_number_typical():
    database = load_correct_database()
    substring = "56"
    search_result = database.search_database(substring)
    assert len(search_result) == 18


def test_database_search_database_number_with_3_digits():
    database = load_correct_database()
    substring = "560"
    search_result = database.search_database(substring)
    assert len(search_result) == 1
    assert search_result[0].get_name() == 'Scrafty'


def test_database_search_database_number_zero():
    database = load_correct_database()
    substring = "0"
    search_result = database.search_database(substring)
    assert isinstance(search_result, type(None))


def test_database_search_database_number_negative():
    database = load_correct_database()
    substring = "-1"
    search_result = database.search_database(substring)
    assert isinstance(search_result, type(None))


def test_database_search_database_number_very_large():
    database = load_correct_database()
    substring = "5000"
    search_result = database.search_database(substring)
    assert isinstance(search_result, type(None))


def test_database_search_database_number_float():
    database = load_correct_database()
    substring = "50.50"
    search_result = database.search_database(substring)
    assert isinstance(search_result, type(None))


def test_database_search_database_query_is_int():
    database = load_correct_database()
    number = 220
    search_result = database.search_database(number)
    assert len(search_result) == 1
    assert search_result[0].get_name() == 'Swinub'


def test_database_search_database_query_invalid_datatype():
    database = load_correct_database()
    number_tuple = (55, 44, 22)
    with raises(BadConversionError):
        database.search_database(number_tuple)


def test_database_get_pokemon_using_name_typical():
    database = load_correct_database()
    name = 'Pikachu'
    pokemon = database.get_pokemon_using_name(name)
    assert pokemon.get_name() == 'Pikachu'


def test_database_get_pokemon_using_name_diffrent_cases():
    database = load_correct_database()
    name = 'PiKAchU'
    pokemon = database.get_pokemon_using_name(name)
    assert pokemon.get_name() == 'Pikachu'


def test_database_get_pokemon_using_name_empty_string():
    database = load_correct_database()
    name = ''
    with raises(DataDoesNotExistError):
        database.get_pokemon_using_name(name)


def test_database_get_pokemon_using_name_not_a_string():
    database = load_correct_database()
    name = 22
    with raises(BadConversionError):
        database.get_pokemon_using_name(name)


def test_database_get_pokemon_using_name_pokemon_does_not_exist():
    database = load_correct_database()
    name = 'PIKAPIKAPIKAPIKACHUUUUU'
    with raises(PokemonDataDoesNotExistError):
        database.get_pokemon_using_name(name)


def test_database_get_pokemon_using_pokedex_number_string_typical():
    database = load_correct_database()
    pokedex_number = '20'
    pokemon = database.get_pokemon_using_pokedex_number(pokedex_number)
    assert pokemon.get_name() == 'Raticate'


def test_database_get_pokemon_using_pokedex_number_string_zero():
    database = load_correct_database()
    pokedex_number = '0'
    with raises(PokemonDataDoesNotExistError):
        database.get_pokemon_using_pokedex_number(pokedex_number)


def test_database_get_pokemon_using_pokedex_number_string_large_number():
    database = load_correct_database()
    pokedex_number = '5000'
    with raises(PokemonDataDoesNotExistError):
        database.get_pokemon_using_pokedex_number(pokedex_number)


def test_database_get_pokemon_using_pokedex_number_string_text():
    database = load_correct_database()
    pokedex_number = 'ala'
    with raises(NotANumberError):
        database.get_pokemon_using_pokedex_number(pokedex_number)


def test_database_get_pokemon_using_pokedex_number_string_float():
    database = load_correct_database()
    pokedex_number = '9.5'
    with raises(BadConversionError):
        database.get_pokemon_using_pokedex_number(pokedex_number)


def test_database_get_pokemon_using_pokedex_number_int_typical():
    database = load_correct_database()
    pokedex_number = 20
    pokemon = database.get_pokemon_using_pokedex_number(pokedex_number)
    assert pokemon.get_name() == 'Raticate'


def test_database_get_pokemon_using_pokedex_number_invalid_datatype():
    database = load_correct_database()
    pokedex_number = 20.60
    with raises(BadConversionError):
        database.get_pokemon_using_pokedex_number(pokedex_number)


def test_search_database_string_name_typical():
    database = load_correct_database()
    name = 'Char'
    pokemon_search_result = database.search_database(name)
    assert len(pokemon_search_result) == 5
    assert pokemon_search_result[0].get_name() == 'Charmander'


def test_search_database_string_name_substring_in_middle_of_string():
    database = load_correct_database()
    name = 'harman'
    pokemon_search_result = database.search_database(name)
    assert len(pokemon_search_result) == 1
    assert pokemon_search_result[0].get_name() == 'Charmander'


def test_search_database_string_name_empty():
    database = load_correct_database()
    name = ''
    pokemon_search_result = database.search_database(name)
    assert len(pokemon_search_result) > 100


def test_search_database_string_name_does_not_exist():
    database = load_correct_database()
    name = 'PIKAPIKAPIKAPIKACHUUU'
    pokemon_search_result = database.search_database(name)
    assert isinstance(pokemon_search_result, type(None))


def test_search_database_string_pokedex_number_string_typical():
    database = load_correct_database()
    no = '25'
    pokemon_search_result = database.search_database(no)
    assert pokemon_search_result[0].get_name() == 'Pikachu'
    assert pokemon_search_result[1].get_name() == 'Electabuzz'


def test_search_database_string_pokedex_number_string_zero():
    database = load_correct_database()
    no = '0'
    pokemon_search_result = database.search_database(no)
    assert isinstance(pokemon_search_result, type(None))


def test_search_database_string_pokedex_number_string_negative():
    database = load_correct_database()
    no = '-1'
    pokemon_search_result = database.search_database(no)
    assert isinstance(pokemon_search_result, type(None))


def test_search_database_string_pokedex_number_string_float():
    database = load_correct_database()
    no = '1.5'
    pokemon_search_result = database.search_database(no)
    assert isinstance(pokemon_search_result, type(None))


def test_search_database_string_pokedex_number_invalid_datatype():
    database = load_correct_database()
    no = 55.55
    with raises(BadConversionError):
        database.search_database(no)
