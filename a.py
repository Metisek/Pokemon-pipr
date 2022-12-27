string = """
                         "pokedex_number",
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
"""

string = string.split('\n')
for i in range(len(string)):
    try:
        x = string[i].replace(',', '')
        x = x.split()
        print('{} : pokemon[{}],'.format(x[0], i-1))
    except:
        pass