from model_io import read_from_json, io_convert_to_int
import re
from classes import (
    PokemonDataDoesNotExistError,
    BadConversionError,
    DataDoesNotExistError,
    BasePokemon,
    NotANumberError
)


class PokemonDatabase:
    """Creating pokemon database as list with BasePokemon objects
       Given database cannot be modified/updated after creation
    """
    def __init__(self, file_path: str) -> None:
        """Creates pokemon database from JSON file given in file_path.\n
        Throws exception if given file is malformed, invalid or missing.

        Args:
            file_path (str): path to given JSON pokemon database

        Raises:
            BadConversionError: Given file_path is not a string.
            DataDoesNotExistError: Given file_path is empty.
            FileNotFoundError: Given file does not exist.
            PermissionError: Given file cannot be accessed.
            IsADirectoryError: Given path is a directory.
            MalformedPokemonDataError: returns type of data corruption
            from JSON file and row where it was found.

        """
        if not isinstance(file_path, str):
            raise BadConversionError('Given path is not a string value')
        if not file_path:
            raise DataDoesNotExistError('Given path value is empty')
        self._pokemon_base = []
        self._base_file_path = file_path
        self._load_from_json()

    def get_pokemon_database_list(self) -> list:
        """ Gets private value of pokemon's database and returns it.

        Returns:
           list : List of BasePokemon objects.
        """
        return self._pokemon_base

    def _get_base_file_path(self) -> str:
        """ Gets private value of file path and returns it.

        Returns:
           str : File path as string.
        """
        return self._base_file_path

    def _set_pokemon_base_list(self, pokemon_base_list: list) -> None:
        """Sets private value of pokemon's database as new database.\n
        Function won't throw exceptio due to parent's function check.

        Args:
            pokemon_base_list (list): list of BasePokemon objects.
        """
        self._pokemon_base = pokemon_base_list

    def _load_from_json(self) -> None:
        """Loads JSON file from given path in __init__.\n
        Throws exception if given file is malformed, invalid or missing.

        Raises:
            FileNotFoundError: Given file does not exist.
            PermissionError: Given file cannot be accessed.
            IsADirectoryError: Given path is a directory.
            MalformedPokemonDataError: returns type of data corruption
            from JSON file and row where it was found.

        """
        try:
            with open(self._get_base_file_path(), 'r') as file_hantle:
                self._set_pokemon_base_list(read_from_json(file_hantle))
        except FileNotFoundError:
            raise FileNotFoundError("Could not open person database.")
        except PermissionError:
            raise PermissionError(
                "You do not have permission to open given file."
                )
        except IsADirectoryError:
            raise IsADirectoryError("Provided path is a directory.")

    def _search_name(self, substring: str) -> list:
        """Searches for every pokemon with matching substring.
        Given search is not case sensitive.\n
        Returns empty list if substring is empty
        or when none of given pokemons contains substring.\n
        For example 'ika' is in 'Pikachu', but not in 'Raichu'.

        Args:
            substring (str): Substring given for search.

        Returns:
            list: List with BasePokemon objects with matching name
        """
        if substring == '' or None:
            return []
        matching_pokemons = []
        pokemons_list = self.get_pokemon_database_list()
        for pokemon in pokemons_list:
            name = pokemon.get_name()
            if re.search(substring, name, re.IGNORECASE):
                matching_pokemons.append(pokemon)
        return matching_pokemons

    def get_pokemon_using_name(self, name: str) -> BasePokemon:
        """Return BasePokemon object using given name.\n
        Thows exception if none of give pokemons has given name.

        Args:
            name (str): Pokemon's name.

        Raises:
            PokemonDataDoesNotExistError: Pokemon with given name does
            not exist.
            BadConversionError: Given name is not a string.

        Returns:
            BasePokemon: Pokemon with matching name
        """
        if not isinstance(name, str):
            raise BadConversionError('Given name is not a string')
        if not name:
            raise DataDoesNotExistError('Given string is empty')
        for pokemon in self.get_pokemon_database_list():
            if re.match(pokemon.get_name(), name, re.IGNORECASE):
                return pokemon
        else:
            raise PokemonDataDoesNotExistError(
                "Pokemon with given name does not exist"
                )

    def _search_pokedex_number(self, number: int) -> list:
        """Searches for every pokemon with given equal or part of number and
        returns list of every matching pokemon.\n
        Pokemon with equal value always appeares first in givel list.\n
        Returns empty list if number is lesser or equal 0, greater than 65535
        or when none of given pokemons has given pokedex_number or it's part.\n
        For example '56' returns list with pokemon '56' as first and '156',
        '256', '356'... as remaining ones.

        Args:
            number (int): Exact or part of pokemon's pokedex_number.

        Returns:
            list: List with BasePokemon objects with matching pokedex_number.
        """
        if number <= 0 or number > 65535:
            return []
        number_as_str = str(number)
        matching_pokemons = []
        pokemons_list = self.get_pokemon_database_list()
        for pokemon in pokemons_list:
            pokedex_number = str(pokemon.get_pokedex_number())
            if pokedex_number == number_as_str:
                matching_pokemons.insert(0, pokemon)
            if len(number_as_str) < len(pokedex_number):
                if number_as_str in pokedex_number:
                    matching_pokemons.append(pokemon)
        return matching_pokemons

    def get_pokemon_using_pokedex_number(
            self, value: (int | str)) -> BasePokemon:
        """Return BasePokemon object using given number.\n
        Thows exception if none of give pokemons has given name.

        Args:
            name (int | str -> int): Pokemon's pokedex_number.

        Raises:
            PokemonDataDoesNotExistError: Pokemon with given name does
            not exist.
            DataDoesNotExistError: Given value is empty
            BadConversionError: Given name is not a string or int, or
            given number is not convertable to int
            NotANumberError: Given string value is not a number

        Returns:
            BasePokemon: Pokemon with matching name
        """
        if not isinstance(value, (int, str)):
            raise BadConversionError('Given name is not a string')
        if not value:
            raise DataDoesNotExistError('Given string is empty')
        try:
            value = io_convert_to_int(value)
        except BadConversionError:
            raise BadConversionError('Given string is a float value')
        except NotANumberError:
            raise NotANumberError('Given string is not a number')

        for pokemon in self.get_pokemon_database_list():
            if pokemon.get_pokedex_number() == value:
                return pokemon
        else:
            raise PokemonDataDoesNotExistError(
                "Pokemon with given pokedex number does not exist"
                )

    def search_database(self, query: (str | int)) -> (list | None):
        """Searches for given query in list of pokemons. If it's a number,
        cheks for pokedex number, otherwise checks for pokemon's name.\n
        Returns list of BasePokemon objects matching criteria or None if
        none of given pokemons match it.\n
        Throws exception only when invalid datatype is given.

        Args:
            query (str | str -> int | int): Any str, str convertable to
            int or in value to search in database

        Raises:
            BadConversionError: Given query value is not a int or str

        Returns:
            list | None: list of BasePokemon objects or None
        """
        if not isinstance(query, (str, int)):
            raise BadConversionError(
                'Given query data type cannot be used for searching'
                )
        if not query:
            return None
        try:
            query = io_convert_to_int(query)
            search_result = self._search_pokedex_number(query)
        except Exception:
            search_result = self._search_name(query)
        if not search_result:
            return None
        return search_result
