import csv
import json


class InvalidFileLineLeghthError(ValueError):
    pass


class MalformedPokemonDataError(Exception):
    pass


def reformat_csv(file, new_file):
    pokemon_list = []
    file_handle = open(file, 'r', encoding='utf-8-sig')
    pokemon_list.append(file_handle.readline())
    for row in file_handle:
        row = row.replace("[", "\"[", 1)
        row = row.replace("]", "]\"", 1)
        pokemon_list.append(row)
    file_handle.close()
    with open(new_file, 'w', encoding='utf-8-sig') as file_hantle:
        file_hantle.writelines(pokemon_list)


def read_from_csv(file):
    pokemon_file = []
    file_handle = open(file, 'r', encoding='utf-8-sig')
    reader = csv.DictReader(file_handle, delimiter=',')
    pokemon_file.append(["pokedex_number",
                         "abilities",
                         "name",
                         "hp",
                         "defense",
                         "attack",
                         "speed",
                         "type1",
                         "type2",
                         "classfication",
                         "experience_growth",
                         "against_bug",
                         "against_dark",
                         "against_dragon",
                         "against_electric",
                         "against_fairy",
                         "against_fight",
                         "against_fire",
                         "against_flying",
                         "against_ghost",
                         "against_grass",
                         "against_ground",
                         "against_ice",
                         "against_normal",
                         "against_poison",
                         "against_psychic",
                         "against_rock",
                         "against_steel",
                         "against_water",
                         "percentage_male",
                         "height_m",
                         "weight_kg",
                         "generation"])
    try:
        for row in reader:
            if len(row) != 41:
                raise InvalidFileLineLeghthError()
            pokedex_number = row['pokedex_number']
            abilities = row['abilities']
            name = row['name']
            hp = row['hp']
            defense = row['defense']
            attack = row['attack']
            speed = row['speed']
            type1 = row['type1']
            type2 = row['type2']
            classfication = row['classfication']
            experience_growth = row['experience_growth']
            against_bug = row['against_bug']
            against_dark = row['against_dark']
            against_dragon = row['against_dragon']
            against_electric = row['against_electric']
            against_fairy = row['against_fairy']
            against_fight = row['against_fight']
            against_fire = row['against_fire']
            against_flying = row['against_flying']
            against_ghost = row['against_ghost']
            against_grass = row['against_grass']
            against_ground = row['against_ground']
            against_ice = row['against_ice']
            against_normal = row['against_normal']
            against_poison = row['against_poison']
            against_psychic = row['against_psychic']
            against_rock = row['against_rock']
            against_steel = row['against_steel']
            against_water = row['against_water']
            percentage_male = row['percentage_male']
            height_m = row['height_m']
            weight_kg = row['weight_kg']
            generation = row['generation']

            if None in row.values():
                raise MalformedPokemonDataError('Missing columns')
            pokemon = [pokedex_number,
                       abilities,
                       name,
                       hp,
                       defense,
                       attack,
                       speed,
                       type1,
                       type2,
                       classfication,
                       experience_growth,
                       against_bug,
                       against_dark,
                       against_dragon,
                       against_electric,
                       against_fairy,
                       against_fight,
                       against_fire,
                       against_flying,
                       against_ghost,
                       against_grass,
                       against_ground,
                       against_ice,
                       against_normal,
                       against_poison,
                       against_psychic,
                       against_rock,
                       against_steel,
                       against_water,
                       percentage_male,
                       height_m,
                       weight_kg,
                       generation
                       ]
            pokemon_file.append(pokemon)
    except csv.Error as e:
        raise MalformedPokemonDataError(str(e))
    file_handle.close()
    return pokemon_file


def write_to_csv(file, pokemon_list):
    file_handle = open(file, 'w', encoding='utf-8-sig')
    writer = csv.DictWriter(file_handle, ["pokedex_number",
                                          "abilities",
                                          "name",
                                          "hp",
                                          "defense",
                                          "attack",
                                          "speed",
                                          "type1",
                                          "type2",
                                          "classfication",
                                          "experience_growth",
                                          "against_bug",
                                          "against_dark",
                                          "against_dragon",
                                          "against_electric",
                                          "against_fairy",
                                          "against_fight",
                                          "against_fire",
                                          "against_flying",
                                          "against_ghost",
                                          "against_grass",
                                          "against_ground",
                                          "against_ice",
                                          "against_normal",
                                          "against_poison",
                                          "against_psychic",
                                          "against_rock",
                                          "against_steel",
                                          "against_water",
                                          "percentage_male",
                                          "height_m",
                                          "weight_kg",
                                          "generation"
                                          ])
    writer.writeheader()
    for pokemon in pokemon_list:
        writer.writerow({
            "pokedex_number": pokemon[0],
            "abilities": pokemon[1],
            "name": pokemon[2],
            "hp": pokemon[3],
            "defense": pokemon[4],
            "attack": pokemon[5],
            "speed": pokemon[6],
            "type1": pokemon[7],
            "type2": pokemon[8],
            "classfication": pokemon[9],
            "experience_growth": pokemon[10],
            "against_bug": pokemon[11],
            "against_dark": pokemon[12],
            "against_dragon": pokemon[13],
            "against_electric": pokemon[14],
            "against_fairy": pokemon[15],
            "against_fight": pokemon[16],
            "against_fire": pokemon[17],
            "against_flying": pokemon[18],
            "against_ghost": pokemon[19],
            "against_grass": pokemon[20],
            "against_ground": pokemon[21],
            "against_ice": pokemon[22],
            "against_normal": pokemon[23],
            "against_poison": pokemon[24],
            "against_psychic": pokemon[25],
            "against_rock": pokemon[26],
            "against_steel": pokemon[27],
            "against_water": pokemon[28],
            "percentage_male": pokemon[29],
            "height_m": pokemon[30],
            "weight_kg": pokemon[31],
            "generation": pokemon[32]
        })
    file_handle.close()


def write_from_csv_to_json(json_file, csv_file):
    data = []
    json_file_handle = open(json_file, 'w', encoding='utf-8')
    csv_file_handle = open(csv_file, 'r', encoding='utf-8-sig')
    reader = csv.DictReader(csv_file_handle, delimiter=',')
    for row in reader:
        if row['pokedex_number'] == 'pokedex_number':
            continue
        if len(row) != 33:
            raise InvalidFileLineLeghthError()
        pokedex_number = row['pokedex_number']
        abilities = row['abilities']
        name = row['name']
        hp = row['hp']
        defense = row['defense']
        attack = row['attack']
        speed = row['speed']
        type1 = row['type1']
        type2 = row['type2']
        classfication = row['classfication']
        experience_growth = row['experience_growth']
        against_bug = row['against_bug']
        against_dark = row['against_dark']
        against_dragon = row['against_dragon']
        against_electric = row['against_electric']
        against_fairy = row['against_fairy']
        against_fight = row['against_fight']
        against_fire = row['against_fire']
        against_flying = row['against_flying']
        against_ghost = row['against_ghost']
        against_grass = row['against_grass']
        against_ground = row['against_ground']
        against_ice = row['against_ice']
        against_normal = row['against_normal']
        against_poison = row['against_poison']
        against_psychic = row['against_psychic']
        against_rock = row['against_rock']
        against_steel = row['against_steel']
        against_water = row['against_water']
        percentage_male = row['percentage_male']
        height_m = row['height_m']
        weight_kg = row['weight_kg']
        generation = row['generation']
        pokemon_data = {
            'pokedex_number': pokedex_number,
            'name': name,
            'abilities': abilities,
            'stats': {
                "hp": hp,
                "defense": defense,
                "attack": attack,
                "speed": speed,
                "type1": type1,
                "type2": type2,
                "classfication": classfication,
                "experience_growth": experience_growth
            },
            'special_strength': {
                "against_bug": against_bug,
                "against_dark": against_dark,
                "against_dragon": against_dragon,
                "against_electric": against_electric,
                "against_fairy": against_fairy,
                "against_fight": against_fight,
                "against_fire": against_fire,
                "against_flying": against_flying,
                "against_ghost": against_ghost,
                "against_grass": against_grass,
                "against_ground": against_ground,
                "against_ice": against_ice,
                "against_normal": against_normal,
                "against_poison": against_poison,
                "against_psychic": against_psychic,
                "against_rock": against_rock,
                "against_steel": against_steel,
                "against_water": against_water,
            },
            'other': {
                "percentage_male": percentage_male,
                "height_m": height_m,
                "weight_kg": weight_kg,
                "generation": generation
            }
        }
        data.append(pokemon_data)
    json.dump(data, json_file_handle, indent=4, ensure_ascii=False)
