from model_io import read_from_json


class PokemonDatabase:

    def __init__(self):
        self._pokemon_base = []

    def get_pokemon_base_list(self):
        return self._pokemon_base

    def set_pokemon_base_list(self, pokemon_base_list):
        self._pokemon_base = pokemon_base_list

    def load_from_json(self, path):
        try:
            with open(path, 'r') as file_hantle:
                self.set_pokemon_base_list(read_from_json(file_hantle))
        except FileNotFoundError:
            raise FileNotFoundError("Could not open person database")
        except PermissionError:
            raise PermissionError(
                "You do not have permission to open given file"
                )
        except IsADirectoryError:
            raise IsADirectoryError("Provided path is a directory")
