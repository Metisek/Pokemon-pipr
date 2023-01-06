from pytest import raises
from classes import BasePokemon, GamePokemon
from classes import (
                     PokemonDataDoesNotExistError,
                     BadConversionError,
                     NotANumberError,
                     #  MalformedPokemonDataError,
                    )
import copy
from database import PokemonDatabase
from math import ceil


def load_correct_database():
    path = 'pokemon.json'
    database = PokemonDatabase(path)
    return database


# Global values for testing purposes:
global pokedex_number
global name
global abilities
global stats
global special_strength
global other

pokedex_number = 1
name = 'Bulbasaur'
abilities = ['Overgrow', 'Chlorophyll']
stats = {
            "hp": "45",
            "defense": "49",
            "attack": "49",
            "speed": "45",
            "type1": "grass",
            "type2": "poison",
            "classfication": "Seed Pokémon",
            "experience_growth": "1059860"
            }
special_strength = {
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
other = {
            "percentage_male": "88.1",
            "height_m": "0.7",
            "weight_kg": "6.9",
            "generation": "1"
        }

# BasePokemon Class


def test_base_pokemon_init():
    pokemon = BasePokemon(pokedex_number, name, abilities,
                          stats, special_strength, other)
    assert pokemon.get_pokedex_number() == 1


def test_base_pokemon_reading_values():
    pokemon = BasePokemon(pokedex_number, name, abilities,
                          stats, special_strength, other)
    assert pokemon.get_pokedex_number() == 1
    assert pokemon.get_base_hp() == 45
    assert pokemon.get_base_attack() == 49
    assert pokemon.get_types() == ('grass', 'poison')
    assert pokemon.get_special_strength_value('bug') == 1.0
    assert pokemon.get_other_value('generation') == 1

# Odpowiedzialność za brakujące/puste dane zrzucamy funkcję wczytującą
# Jest to kluczowe w przypadku każdej zmiennej która ma str oraz list abilities
# Liczby i tak zostają tu konwertowane dla wygody
# Klasa jest za to odpowiedzialna za poprawną konwersję typów


def test_base_pokemon_non_convertable_string_to_int():
    new_pokedex_number = 'test'
    with raises(NotANumberError):
        BasePokemon(new_pokedex_number, name, abilities,
                    stats, special_strength, other)


def test_base_pokemon_hp_stat_non_convertable():
    new_stats = copy.deepcopy(stats)
    new_stats['hp'] = 'essa'
    with raises(NotANumberError):
        BasePokemon(pokedex_number, name, abilities,
                    new_stats, special_strength, other)


def test_base_pokemon_hp_stat_equals_zero():
    new_stats = copy.deepcopy(stats)
    new_stats['hp'] = 0
    with raises(ValueError):
        BasePokemon(pokedex_number, name, abilities,
                    new_stats, special_strength, other)


def test_base_pokemon_hp_stat_negative():
    new_stats = copy.deepcopy(stats)
    new_stats['hp'] = -1
    with raises(ValueError):
        BasePokemon(pokedex_number, name, abilities,
                    new_stats, special_strength, other)


def test_base_pokemon_hp_stat_is_float():
    new_stats = copy.deepcopy(stats)
    new_stats['hp'] = 2.5
    with raises(BadConversionError):
        BasePokemon(pokedex_number, name, abilities,
                    new_stats, special_strength, other)

# Testów dla pozostałych zmiennych nie trzeba pisać bo są podobne


def test_base_pokemon_get_special_dict():
    pokemon = BasePokemon(pokedex_number, name, abilities,
                          stats, special_strength, other)
    specials = pokemon.get_special_strength_dict()
    assert specials['against_bug'] == 1.0
    assert specials['against_fire'] == 2.0


def test_base_pokemon_get_special_vals_typical():
    pokemon = BasePokemon(pokedex_number, name, abilities,
                          stats, special_strength, other)
    assert pokemon.get_special_strength_value('bug') == 1.0
    assert pokemon.get_special_strength_value('fire') == 2.0


def test_base_pokemon_get_special_vals_wrong_type():
    pokemon = BasePokemon(pokedex_number, name, abilities,
                          stats, special_strength, other)
    with raises(PokemonDataDoesNotExistError):
        pokemon.get_special_strength_value('academic')


def test_base_pokemon_empty_other_dict_vals_except_generation():
    new_other = copy.deepcopy(other)
    new_other['percentage_male'] = None
    new_other['height_m'] = None
    new_other['weight_kg'] = None
    base_pokemon = BasePokemon(pokedex_number, name, abilities,
                               stats, special_strength, new_other)
    assert base_pokemon.get_other_value('height_m') is None
    assert base_pokemon.get_other_value('weight_kg') is None
    assert base_pokemon.get_other_value('percentage_male') is None


def test_game_pokemon_init_typical():
    base_pokemon = BasePokemon(pokedex_number, name, abilities,
                               stats, special_strength, other)
    game_pokemon = GamePokemon(base_pokemon)
    assert game_pokemon.get_max_hp() == 45
    assert game_pokemon.get_hp() == 45
    assert game_pokemon.get_attack() == 49
    assert game_pokemon.get_defense() == 49
    assert game_pokemon.get_speed() == 45


def test_game_pokemon_init_not_random_other_values():
    base_pokemon = BasePokemon(pokedex_number, name, abilities,
                               stats, special_strength, other)
    game_pokemon = GamePokemon(base_pokemon, False)
    assert game_pokemon.get_max_hp() == 45
    assert game_pokemon.get_gender() == 'Male'
    assert game_pokemon.get_height() == 0.7
    assert game_pokemon.get_weight() == 6.9


def test_game_pokemon_init_random_other_values(monkeypatch):

    def double_given_value(x, y):
        return 200
    monkeypatch.setattr("classes.randint", double_given_value)
    base_pokemon = BasePokemon(pokedex_number, name, abilities,
                               stats, special_strength, other)
    game_pokemon = GamePokemon(base_pokemon)
    assert game_pokemon.get_max_hp() == 45
    assert game_pokemon.get_gender() == 'Male'
    assert game_pokemon.get_height() == 1.4
    assert game_pokemon.get_weight() == 13.8


def test_game_pokemon_set_hp_typical():
    base_pokemon = BasePokemon(pokedex_number, name, abilities,
                               stats, special_strength, other)
    game_pokemon = GamePokemon(base_pokemon, False)
    assert game_pokemon.get_hp() == 45
    game_pokemon.set_hp(55)
    assert game_pokemon.get_hp() == 55
    assert game_pokemon.get_is_alive() == 1  # True


def test_game_pokemon_set_hp_float():
    base_pokemon = BasePokemon(pokedex_number, name, abilities,
                               stats, special_strength, other)
    game_pokemon = GamePokemon(base_pokemon, False)
    with raises(ValueError):
        game_pokemon.set_hp(20.4)


def test_game_pokemon_set_hp_zero():
    base_pokemon = BasePokemon(pokedex_number, name, abilities,
                               stats, special_strength, other)
    game_pokemon = GamePokemon(base_pokemon, False)
    game_pokemon.set_hp(0)
    assert game_pokemon.get_hp() == 0
    assert game_pokemon.get_is_alive() == 0  # False


def test_game_pokemon_set_hp_negative():
    base_pokemon = BasePokemon(pokedex_number, name, abilities,
                               stats, special_strength, other)
    game_pokemon = GamePokemon(base_pokemon, False)
    with raises(ValueError):
        game_pokemon.set_hp(-2)


def test_game_pokemon_set_max_hp_typical():
    base_pokemon = BasePokemon(pokedex_number, name, abilities,
                               stats, special_strength, other)
    game_pokemon = GamePokemon(base_pokemon, False)
    assert game_pokemon.get_max_hp() == 45
    game_pokemon.set_max_hp(55)
    assert game_pokemon.get_max_hp() == 55


def test_game_pokemon_set_max_hp_lower_than_current_hp():
    base_pokemon = BasePokemon(pokedex_number, name, abilities,
                               stats, special_strength, other)
    game_pokemon = GamePokemon(base_pokemon, False)
    assert game_pokemon.get_max_hp() == 45
    assert game_pokemon.get_hp() == 45
    game_pokemon.set_max_hp(20)
    assert game_pokemon.get_max_hp() == 20
    assert game_pokemon.get_hp() == 20


def test_game_pokemon_set_max_hp_float():
    base_pokemon = BasePokemon(pokedex_number, name, abilities,
                               stats, special_strength, other)
    game_pokemon = GamePokemon(base_pokemon, False)
    with raises(ValueError):
        game_pokemon.set_max_hp(20.4)


def test_game_pokemon_set_max_hp_zero():
    base_pokemon = BasePokemon(pokedex_number, name, abilities,
                               stats, special_strength, other)
    game_pokemon = GamePokemon(base_pokemon, False)
    with raises(ValueError):
        game_pokemon.set_max_hp(0)


def test_game_pokemon_set_max_hp_negative():
    base_pokemon = BasePokemon(pokedex_number, name, abilities,
                               stats, special_strength, other)
    game_pokemon = GamePokemon(base_pokemon, False)
    with raises(ValueError):
        game_pokemon.set_max_hp(-2)


def test_game_pokemon_set_attack_typical():
    base_pokemon = BasePokemon(pokedex_number, name, abilities,
                               stats, special_strength, other)
    game_pokemon = GamePokemon(base_pokemon, False)
    assert game_pokemon.get_attack() == 49
    game_pokemon.set_attack(55)
    assert game_pokemon.get_attack() == 55


def test_game_pokemon_set_attack_float():
    base_pokemon = BasePokemon(pokedex_number, name, abilities,
                               stats, special_strength, other)
    game_pokemon = GamePokemon(base_pokemon, False)
    with raises(ValueError):
        game_pokemon.set_attack(20.4)


def test_game_pokemon_set_attack_zero():
    base_pokemon = BasePokemon(pokedex_number, name, abilities,
                               stats, special_strength, other)
    game_pokemon = GamePokemon(base_pokemon, False)
    game_pokemon.set_attack(0)
    assert game_pokemon.get_attack() == 0


def test_game_pokemon_set_attack_negative():
    base_pokemon = BasePokemon(pokedex_number, name, abilities,
                               stats, special_strength, other)
    game_pokemon = GamePokemon(base_pokemon, False)
    with raises(ValueError):
        game_pokemon.set_attack(-2)


def test_game_pokemon_set_defense_typical():
    base_pokemon = BasePokemon(pokedex_number, name, abilities,
                               stats, special_strength, other)
    game_pokemon = GamePokemon(base_pokemon, False)
    assert game_pokemon.get_defense() == 49
    game_pokemon.set_defense(55)
    assert game_pokemon.get_defense() == 55


def test_game_pokemon_set_defense_float():
    base_pokemon = BasePokemon(pokedex_number, name, abilities,
                               stats, special_strength, other)
    game_pokemon = GamePokemon(base_pokemon, False)
    with raises(ValueError):
        game_pokemon.set_defense(20.4)


def test_game_pokemon_set_defense_zero():
    base_pokemon = BasePokemon(pokedex_number, name, abilities,
                               stats, special_strength, other)
    game_pokemon = GamePokemon(base_pokemon, False)
    with raises(ValueError):
        game_pokemon.set_defense(0)


def test_game_pokemon_set_defense_negative():
    base_pokemon = BasePokemon(pokedex_number, name, abilities,
                               stats, special_strength, other)
    game_pokemon = GamePokemon(base_pokemon, False)
    with raises(ValueError):
        game_pokemon.set_defense(-2)


def test_game_pokemon_empty_other_dict_vals_except_generation():
    new_other = copy.deepcopy(other)
    new_other['percentage_male'] = None
    new_other['height_m'] = None
    new_other['weight_kg'] = None
    base_pokemon = BasePokemon(pokedex_number, name, abilities,
                               stats, special_strength, new_other)
    game_pokemon = GamePokemon(base_pokemon)
    assert game_pokemon.get_gender() == 'Unknown'
    assert game_pokemon.get_height() is None
    assert game_pokemon.get_weight() is None


def test_game_pokemon_base_attack_algorithm_stab_1(monkeypatch):
    database = load_correct_database()
    pokemon_list = database.get_pokemon_database_list()
    player_pokemon = GamePokemon(pokemon_list[0])
    enemy_pokemon = GamePokemon(pokemon_list[1])
    assert player_pokemon.get_attack() == 49
    assert enemy_pokemon.get_defense() == 63

    def always_255(x, y):
        return 255

    monkeypatch.setattr("classes.randint", always_255)
    attack_val = ceil(
        player_pokemon._base_attack_algorithm(enemy_pokemon, 1, 1)
    )
    assert attack_val == 3


def test_game_pokemon_base_attack_algorithm_stab_1_5(monkeypatch):
    database = load_correct_database()
    pokemon_list = database.get_pokemon_database_list()
    player_pokemon = GamePokemon(pokemon_list[0])
    enemy_pokemon = GamePokemon(pokemon_list[1])
    assert player_pokemon.get_attack() == 49
    assert enemy_pokemon.get_defense() == 63

    def always_255(x, y):
        return 255

    monkeypatch.setattr("classes.randint", always_255)
    attack_val = ceil(
        player_pokemon._base_attack_algorithm(enemy_pokemon, 1.5, 1)
    )
    assert attack_val == 5


def test_game_pokemon_special_attack_algorithm_stab_1(monkeypatch):
    database = load_correct_database()
    pokemon_list = database.get_pokemon_database_list()
    player_pokemon = GamePokemon(pokemon_list[0])
    enemy_pokemon = GamePokemon(pokemon_list[1])
    assert player_pokemon.get_attack() == 49
    assert enemy_pokemon.get_defense() == 63
    enemy_types = enemy_pokemon.get_types()
    assert player_pokemon.get_special_strength_value(
        enemy_types[0]) == 0.25
    assert player_pokemon.get_special_strength_value(
        enemy_types[1]) == 1

    def always_255(x, y):
        return 255

    monkeypatch.setattr("classes.randint", always_255)
    attack_val = ceil(
        player_pokemon._special_attack_algotithm(enemy_pokemon, 1, 1)
    )
    assert attack_val == 1


def test_game_pokemon_special_attack_algorithm_stab_1_5(monkeypatch):
    database = load_correct_database()
    pokemon_list = database.get_pokemon_database_list()
    player_pokemon = GamePokemon(pokemon_list[0])
    enemy_pokemon = GamePokemon(pokemon_list[1])
    assert player_pokemon.get_attack() == 49
    assert enemy_pokemon.get_defense() == 63
    enemy_types = enemy_pokemon.get_types()
    assert player_pokemon.get_special_strength_value(
        enemy_types[0]) == 0.25
    assert player_pokemon.get_special_strength_value(
        enemy_types[1]) == 1

    def always_255(x, y):
        return 255

    monkeypatch.setattr("classes.randint", always_255)
    attack_val = ceil(
        player_pokemon._special_attack_algotithm(enemy_pokemon, 1.5, 1)
    )
    assert attack_val == 2


def test_game_pokemon_base_attack_algorithm_stab_1_5_crit(monkeypatch):
    database = load_correct_database()
    pokemon_list = database.get_pokemon_database_list()
    player_pokemon = GamePokemon(pokemon_list[0])
    enemy_pokemon = GamePokemon(pokemon_list[1])
    assert player_pokemon.get_attack() == 49
    assert enemy_pokemon.get_defense() == 63

    def always_255(x, y):
        return 255

    monkeypatch.setattr("classes.randint", always_255)
    attack_val = ceil(
        player_pokemon._base_attack_algorithm(enemy_pokemon, 1.5, 2)
    )
    assert attack_val == 6


def test_game_pokemon_increase_defense():
    database = load_correct_database()
    pokemon_list = database.get_pokemon_database_list()
    player_pokemon = GamePokemon(pokemon_list[0])
    assert player_pokemon.get_defense() == 49
    player_pokemon.increase_defense()
    assert player_pokemon.get_defense() == 54
    player_pokemon.increase_defense()
    assert player_pokemon.get_defense() == 59
    player_pokemon.increase_defense()
    assert player_pokemon.get_defense() == 64
    player_pokemon.increase_defense()
    assert player_pokemon.get_defense() == 69
