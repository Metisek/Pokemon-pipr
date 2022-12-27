from pytest import raises
from classes import BasePokemon
from classes import MalformedPokemonDataError
import copy

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


def test_create_pokemon_typical():
    pokemon = BasePokemon(pokedex_number, name, abilities,
                          stats, special_strength, other)
    assert pokemon.get_pokedex_number() == 1


def test_create_pokemon_reading_values():
    pokemon = BasePokemon(pokedex_number, name, abilities,
                          stats, special_strength, other)
    assert pokemon.get_pokedex_number() == 1
    assert pokemon.get_hp() == 45
    assert pokemon.get_attack() == 49
    assert pokemon.get_types() == ['grass', 'poison']
    assert pokemon.get_special_strength_value('bug') == 1.0
    assert pokemon.get_other_value('generation') == 1

# Odpowiedzialność za brakujące/puste dane zrzucamy na inną funkcję wczytującą
# Jest to kluczowe w przypadku każdej zmiennej która ma str oraz list abilities
# Liczby i tak zostają tu konwertowane dla wygody
# Klasa jest za to odpowiedzialna za poprawną konwersję typów


def test_create_pokemon_non_convertable_string_to_int():
    new_pokedex_number = ''
    with raises(MalformedPokemonDataError):
        BasePokemon(new_pokedex_number, name, abilities,
                    stats, special_strength, other)


def test_create_pokemon_hp_stat_non_convertable():
    new_stats = copy.deepcopy(stats)
    new_stats['hp'] = 'essa'
    with raises(MalformedPokemonDataError):
        BasePokemon(pokedex_number, name, abilities,
                    new_stats, special_strength, other)


def test_create_pokemon_hp_stat_equals_zero():
    new_stats = copy.deepcopy(stats)
    new_stats['hp'] = 0
    with raises(MalformedPokemonDataError):
        BasePokemon(pokedex_number, name, abilities,
                    new_stats, special_strength, other)



def test_create_pokemon_hp_stat_negative():
    new_stats = copy.deepcopy(stats)
    new_stats['hp'] = -1
    with raises(MalformedPokemonDataError):
        BasePokemon(pokedex_number, name, abilities,
                    new_stats, special_strength, other)


def test_create_pokemon_hp_stat_is_float():
    new_stats = copy.deepcopy(stats)
    new_stats['hp'] = 0.5
    with raises(MalformedPokemonDataError):
        BasePokemon(pokedex_number, name, abilities,
                    new_stats, special_strength, other)



def test_set_attack_typical():
    pokemon = BasePokemon(pokedex_number, name, abilities,
                          stats, special_strength, other)
    assert pokemon.get_attack() == 49
    pokemon.set_attack(54)
    assert pokemon.get_attack() == 54

 
def test_set_attack_equal_zero():
    pokemon = BasePokemon(pokedex_number, name, abilities,
                          stats, special_strength, other)
    with raises(MalformedPokemonDataError):
        pokemon.set_attack(0)


def test_set_attack_negative():
    pokemon = BasePokemon(pokedex_number, name, abilities,
                          stats, special_strength, other)
    with raises(MalformedPokemonDataError):
        pokemon.set_attack(-2)
        

def test_set_attack_float():
    pokemon = BasePokemon(pokedex_number, name, abilities,
                          stats, special_strength, other)
    with raises(MalformedPokemonDataError):
        pokemon.set_attack(2.5)
        

def test_set_attack_wrong_datatype():
    pokemon = BasePokemon(pokedex_number, name, abilities,
                          stats, special_strength, other)
    with raises(MalformedPokemonDataError):
        pokemon.set_attack('test')
