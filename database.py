from reference.database_convertion import(
    read_from_csv, 
    write_to_csv, 
    read_from_json, 
    write_to_json
)


class PersonPathNotFound(FileNotFoundError):
    pass


class PersonPathIsADirectory(IsADirectoryError):
    pass


class PersonPermissionError(PermissionError):
    pass


class Database:

    def __init__(self):
        self._people = []

    def get_people(self):
        return self._people

    def set_people(self, people):
        self._people = people

    def load_from_csv(self, path):
        try:
            with open(path, 'r') as file_hantle:
                self.set_people(read_from_csv(file_hantle))
        except FileNotFoundError:
            raise PersonPathNotFound("Could not open person database")
        except PermissionError:
            raise PersonPermissionError(
                "You do not have permission to open database file"
                )
        except IsADirectoryError:
            raise PersonPathIsADirectory("Provided path is a directory")

    def save_to_csv(self, path):
        try:
            with open(path, 'w') as file_hantle:
                write_to_csv(file_hantle, self.get_people())
        except PermissionError:
            raise PersonPermissionError(
                "You do not have permission to write database file"
                )
        except IsADirectoryError:
            raise PersonPathIsADirectory("Provided path is a directory")
        
    def load_from_json(self, path):
        try:
            with open(path, 'r') as file_hantle:
                self.set_people(read_from_json(file_hantle))
        except FileNotFoundError:
            raise PersonPathNotFound("Could not open person database")
        except PermissionError:
            raise PersonPermissionError(
                "You do not have permission to open database file"
                )
        except IsADirectoryError:
            raise PersonPathIsADirectory("Provided path is a directory")

    def save_to_json(self, path):
        try:
            with open(path, 'w') as file_hantle:
                write_to_json(file_hantle, self.get_people())
        except PermissionError:
            raise PersonPermissionError(
                "You do not have permission to write database file"
                )
        except IsADirectoryError:
            raise PersonPathIsADirectory("Provided path is a directory")
