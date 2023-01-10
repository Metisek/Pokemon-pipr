import tkinter as tk
from database import PokemonDatabase
from attributes import DATABASE_PATH
from classes import BasePokemon
from classes import (
    InvalidDataTypeError,
    InvalidObjectTypeError,
    MalformedDataError,
    NotANumberError
)
from tkinter import ttk


class TkPokemonSelectWindow:
    """Tk window object that allows adding pokemon to pygame
    from embedded database using file specified in attributes
    DATABASE_PATH
    """
    def __init__(self) -> None:
        """Initialises window object without showing it with
        saved BasePokemon database using file specified in attributes
        DATABASE_PATH

        Raises:
            BadConversionError: Given file_path is not a string.
            DataDoesNotExistError: Given file_path is empty.
            FileNotFoundError: Given file does not exist.
            PermissionError: Given file cannot be accessed.
            IsADirectoryError: Given path is a directory.
            MalformedPokemonDataError: returns type of data corruption
            from JSON file and row where it was found.
        """
        self._database = PokemonDatabase(DATABASE_PATH)
        self._database_values = self.get_full_database()
        self._database_tree_view = None
        self._window = None
        self._selected_pokemon = None
        self._choosen_pokemon = None

    def get_full_database(self) -> list[BasePokemon]:
        """Gets list with all BasePokemon objects and returns it

        Returns:
            list[*BasePokemon]: List with all saved BasePokemon objects
        """
        data = self._database.get_pokemon_database_list()
        return data

    def get_database_values(self) -> list[BasePokemon]:
        """Gets currently saved/searched list of BasePokemon objects
        and returns it

        Returns:
            list[*BasePokemon]: List with currently searched BasePokemon
            objects
        """
        return self._database_values

    def get_selected_pokemon(self) -> (int | None):
        """Gets pokedex_nember of selected BasePokemon in TreeView or
        returns None is No value is selected

        Returns:
            int | None: Current pokedex_number
        """
        return self._selected_pokemon

    def _get_tree_view(self) -> ttk.Treeview:
        """Gets ttk.TreeView object from current window

        Returns:
            ttk.Treeview: ttk.TreeView active widget
        """
        return self._database_tree_view

    def _set_tree_view(self, object: ttk.Treeview) -> None:
        """Sets private database treeview object to given object

        Args:
            object (ttk.Treeview): _description_

        Raises:
            InvalidObjectTypeError: Given object is not ttk.Treeview
            object
        """
        if not isinstance(object, ttk.Treeview):
            raise InvalidObjectTypeError(
                'Given object is not a ttk.TreeView object'
                )
        self._database_tree_view = object

    def get_choosen_pokemon(self) -> BasePokemon | None:
        """Returns choosen pokemon if it was added or none if
        window was closed or cancelled

        Returns:
            BasePokemon | None: Choosen pokemon or None if not added
        """
        if isinstance(self._choosen_pokemon, type(None)):
            return self._choosen_pokemon
        try:
            self._choosen_pokemon = int(self._choosen_pokemon)
            pokemon = self._database.get_pokemon_using_pokedex_number(
                self._choosen_pokemon
                )
        except NotANumberError:
            pokemon = self._database.get_pokemon_using_name(
                self._choosen_pokemon
                )
        return pokemon

    def _get_window(self) -> (tk.Tk | None):
        """Gets currently open window or None is not opened

        Returns:
            tk.Tk: Currently open window or None if inactive
        """
        return self._window

    def _set_database_values(self, values: (list[BasePokemon] | None)) -> None:
        """Sets active database values to those given in values.
        Throws exception if given value is malformed or in not iterable

        Args:
            values (list[BasePokemon]): List of BasePokemon objects

        Raises:
            InvalidDataTypeError: Given argument is not a
            list or tuple, or None for empty list'
            MalformedDataError: Given list contains malformed data
        """
        try:
            if not isinstance(values, (list, tuple, type(None))):
                raise InvalidDataTypeError
            if not isinstance(values, type(None)):
                for pokemon in values:
                    if not isinstance(pokemon, BasePokemon):
                        raise MalformedDataError
            else:
                values = []
        except InvalidDataTypeError:
            raise InvalidDataTypeError(
                'Given argument is not a list or tuple, or None for empty list'
                )
        except MalformedDataError:
            raise MalformedDataError('Given list contains malformed data')

        self._database_values = values

    def _set_window(self, window: tk.Tk | None):
        """Sets current active window to specified tk window or
        None is it's destroyed.

        Args:
            window (tk.Tk | None): tk.Tk window or None if destryed
        """
        self._window = window

    def _set_chosen_pokemon(self, pokemon: (BasePokemon | None)) -> None:
        """Sets choosen pokemon to givrn BasePokemon object or None
        if adding pokemon process is cancelled.

        Args:
            pokemon (BasePokemon): BasePokemon object
        """
        self._choosen_pokemon = pokemon

    def set_selected_pokemon(self, value: (int | None)) -> None:
        """Sets currently selected pokemon from TreeView as pokemon's
        pokedex_number or None if it's not selected.

        Args:
            value (int | None): pokedex_number value
        """
        self._selected_pokemon = value

    def terminate_window(self):
        """Destroys current window while saving object's values
        """
        window = self._get_window()
        window.destroy()
        self._set_window(None)

    def _change_values_in_listbox(self, database_tree: ttk.Treeview) -> None:
        """Changes values in given TreeView list using saved database values

        Args:
            database_tree (ttk.Treeview): Active widget with database
        """
        self.set_selected_pokemon(None)
        for elem in database_tree.get_children():
            database_tree.delete(elem)
        data = self.get_database_values()
        if data:
            for elem in data:
                pokedex_number = str(elem.get_pokedex_number())
                pokemon_name = str(elem.get_name())
                hp = str(elem.get_base_hp())
                attack = str(elem.get_base_attack())
                defense = str(elem.get_base_defense())
                speed = str(elem.get_base_speed())
                types = elem.get_types()
                types_str = str('{}, {}'.format(types[0], types[1]) if types[1]
                                else '{}'.format(types[0]))
                database_tree.insert(
                    parent='', index=tk.END, iid=int(pokedex_number), values=(
                        pokedex_number, pokemon_name, hp,
                        attack, defense, speed, types_str)
                    )

    # Button commands

    def add_pokemon(self) -> None:
        """Button command: Returns currentl selected pokemon
        as BasePokemon object if it's selcted, does nothing otherwise.
        """
        if self.get_selected_pokemon():
            self._set_chosen_pokemon(self.get_selected_pokemon())
            self.set_selected_pokemon(None)
            self.terminate_window()

    def cancel_adding(self) -> None:
        """Exits window without changing anything
        """
        self._set_chosen_pokemon(None)
        self.terminate_window()

    def search_database(self, query: str, database_tree: ttk.Treeview):
        """Searches database using given query and updates TreeView

        Args:
            query (str): Any search input
            database_tree (ttk.Treeview): ttk.Treeview with database vals
        """
        data = self._database.search_database(query)
        self._set_database_values(data)
        self._change_values_in_listbox(database_tree)

    def select_new_pokemon(self, x) -> None:
        """Selects new pokemon after select event in ttk.TreeView

        Args:
            x (_type_): Filler argument, does nothing
        """
        selected = self._get_tree_view().selection()[0]
        item = self._get_tree_view().item(selected)
        self.set_selected_pokemon(item.get('values')[0])

    def show_window(self):
        """Makes window appear on screen
        """
        self.make_window()
        window = self._get_window()
        window.mainloop()

    def make_window(self):
        """Initialises window layout using saved values and
        functions inside this class.
        """
        self._set_chosen_pokemon(None)
        self._set_database_values(self.get_full_database())

        win = tk.Tk()
        win.geometry('600x330')
        win.resizable(False, False)
        win.title("Add pokemon")

        # Database frame
        database_frame = tk.Frame(win)
        database_frame.pack(fill=tk.BOTH, side=tk.TOP)

        scroll = tk.Scrollbar(database_frame, orient=tk.VERTICAL)
        database = ttk.Treeview(
            database_frame, yscrollcommand=scroll.set, height=12
            )
        database['columns'] = (
            'pokedex_id', 'name', 'base_hp', 'base_attack',
            'base_defense', 'base_speed', 'pokemon_types'
            )
        database.column("#0", width=0,  stretch=tk.NO)
        database.column("pokedex_id", anchor=tk.CENTER, width=30)
        database.column("name", anchor=tk.CENTER, width=130)
        database.column("base_hp", anchor=tk.CENTER, width=35)
        database.column("base_attack", anchor=tk.CENTER, width=35)
        database.column("base_defense", anchor=tk.CENTER, width=35)
        database.column("base_speed", anchor=tk.CENTER, width=35)
        database.column("pokemon_types", anchor=tk.CENTER, width=205)

        database.heading("#0", text='', anchor=tk.CENTER)
        database.heading("pokedex_id", anchor=tk.CENTER, text='ID')
        database.heading("name", anchor=tk.CENTER, text='Pokemon name')
        database.heading("base_hp", anchor=tk.CENTER, text='HP')
        database.heading("base_attack", anchor=tk.CENTER, text='ATT')
        database.heading("base_defense", anchor=tk.CENTER, text='DEF')
        database.heading("base_speed", anchor=tk.CENTER, text='SPD')
        database.heading(
            "pokemon_types", anchor=tk.CENTER, text='Pokemon types'
            )
        self._set_tree_view(database)
        self._change_values_in_listbox(self._get_tree_view())

        database.bind("<<TreeviewSelect>>", self.select_new_pokemon)

        scroll.config(command=database.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        database.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        search_frame = tk.Frame(win)
        search_frame.pack()

        tk.Label(search_frame, text="Search with ID or name:").grid(
            row=0, column=0, sticky=tk.W
            )
        query_input = tk.StringVar()
        search = tk.Entry(search_frame, textvariable=query_input, width=30)
        search_button = tk.Button(
            search_frame, text="Search",
            command=lambda: self.search_database(
                query_input.get(), self._get_tree_view()),
            padx=5
            )
        search.grid(row=0, column=1, sticky=tk.W)
        search_button.grid(row=0, column=2, sticky=tk.E)

        command_frame = tk.Frame(win)       # Row of buttons
        command_frame.pack()
        add_button = tk.Button(
            command_frame, text=" Add pokemon", command=self.add_pokemon
            )
        cancel_button = tk.Button(
            command_frame, text="Cancel", command=self.cancel_adding
            )
        add_button.pack(side=tk.LEFT)
        cancel_button.pack(side=tk.LEFT)

        self._set_window(win)
