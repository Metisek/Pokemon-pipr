import csv
import json

class InvalidFileLineLeghthError(ValueError):
    pass


class MalformedPersonDataError(Exception):
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
    pokemon_list = []
    file_handle = open(file, 'r', encoding='utf-8-sig')
    reader = csv.DictReader(file_handle, delimiter=',')
    try:
        for row in reader:
            pokedex_number = row['pokedex_number']
            name = row['name']
            hp = row['hp']
            defense = row['defense']
            classfication = row['classfication']
            against_bug	= row['against_bug']
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

            if None in row.values():
                raise MalformedPersonDataError('Missing columns')
    except csv.Error as e:
        raise MalformedPersonDataError(str(e))
    file_handle.close()
    return pokemon_list


# def write_to_csv(file_handle, people):
#     writer = csv.DictWriter(file_handle, ['id', 'name', 'sex', 'birth_date'])
#     writer.writeheader()
#     for person in people:
#         id = person.get_id()
#         name = person.get_name()
#         sex = person.get_sex()
#         birth_date = person.get_birth_date()
#         writer.writerow({
#             'id': id,
#             'name': name,
#             'sex': sex,
#             'birth_date': birth_date
#         })


# def read_from_json(file_handle):
#     people = []
#     data = json.load(file_handle)
#     for item in data:
#         try:
#             id = item['id']
#             name = item['name']
#             sex = item['sex']
#             birth_date = item['birth_date']
#             person = Person(id, name, sex, birth_date)
#         except KeyError as e:
#             raise MalformedPersonDataError('Missing key in file') from e
#         except Exception as e:
#             raise InvalidPersonError(item) from e
#         people.append(person)
#     return people


# def write_to_json(file_handle, people):
#     data = []
#     for person in people:
#         id = person.get_id()
#         name = person.get_name()
#         sex = person.get_sex()
#         birth_date = person.get_birth_date()
#         person_data = {
#             'id': id,
#             'name': name,
#             'sex': sex,
#             'birth_date': birth_date
#         }
#         data.append(person_data)
#     json.dump(data, file_handle, indent=4)
