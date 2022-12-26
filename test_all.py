# Placeholder tymczasowy
# from main import *
# from classes import *
from reference.database_convertion import read_from_csv, reformat_csv

def test_tests():
    assert True == True
    
def test_creating_reformatted_file():
    file = 'reference/pokemon.csv'
    new_file = 'reference/reformatted_pokemon.csv'
    pokemon_list = reformat_csv(file, new_file)
    
def test_reading_reformatted_file():
    file = 'reference/reformatted_pokemon.csv'
    pokemon_list = read_from_csv(file)