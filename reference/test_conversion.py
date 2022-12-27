# Placeholder tymczasowy
# from main import *
# from classes import *
from reference.database_convertion import write_from_csv_to_json, read_from_csv, reformat_csv, write_to_csv

def test_tests():
    assert True == True
    
def test_creating_reformatted_file():
    file = 'reference/pokemon.csv'
    new_file = 'reference/reformatted_pokemon.csv'
    pokemon_list = reformat_csv(file, new_file)
    
def test_reading_reformatted_file():
    file = 'reference/reformatted_pokemon.csv'
    pokemon_list = read_from_csv(file)
    assert pokemon_list[1][0] == 1
    
def test_writing_modified_csv_file():
    file = 'reference/reformatted_pokemon.csv'
    new_file = 'reference/cleaned_pokemon.csv'
    pokemon_list = read_from_csv(file)
    write_to_csv(new_file, pokemon_list)

def test_writing_final_json_file():
    json_file = 'reference/final_pokemon.json'
    csv_file = 'reference/cleaned_pokemon.csv'
    write_from_csv_to_json(json_file, csv_file)