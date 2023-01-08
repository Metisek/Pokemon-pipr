import tkinter as tk
from database import PokemonDatabase
from attributes import DATABASE_PATH
from classes import BasePokemon
from tkinter import ttk


class TkPokemonSelectWindow:
    def __init__(self) -> None:
        self._database = PokemonDatabase(DATABASE_PATH)
        self._database_values = self.get_full_database()
        self._database_tree_view = None
        self._window = None
        self._selected_pokemon = None
        self._choosen_pokemon = None

    def get_full_database(self):
        data = self._database.get_pokemon_database_list()
        return data

    def get_database_values(self):
        return self._database_values

    def get_selected_pokemon(self):
        return self._selected_pokemon

    def _get_tree_view(self):
        return self._database_tree_view

    def _set_tree_view(self, val):
        self._database_tree_view = val

    def get_choosen_pokemon(self):
        return self._choosen_pokemon

    def _get_window(self) -> tk.Tk:
        return self._window

    def _set_database_values(self, values: list[BasePokemon]):
        self._database_values = values

    def _set_window(self, window):
        self._window = window

    def _set_chosen_pokemon(self, pokemon: BasePokemon):
        self._choosen_pokemon = pokemon

    def set_selected_pokemon(self, value):
        self._selected_pokemon = value

    def terminate_window(self):
        window = self._get_window()
        window.destroy()
        self._set_window(None)

    def change_values_in_listbox(self, database_tree: ttk.Treeview):
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

    def add_pokemon(self):
        if self.get_selected_pokemon():
            self._set_chosen_pokemon(self.get_selected_pokemon())
            self.set_selected_pokemon(None)
            self.terminate_window()

    def cancel_adding(self):
        self._set_chosen_pokemon(None)
        self.terminate_window()

    def search_database(self, query, database_tree: ttk.Treeview):
        data = self._database.search_database(query)
        self._set_database_values(data)
        self.change_values_in_listbox(database_tree)

    def select_new_pokemon(self, x):
        selected = self._get_tree_view().selection()[0]
        item = self._get_tree_view().item(selected)
        self.set_selected_pokemon(item.get('values')[0])

    def show_window(self):
        self.make_window()
        window = self._get_window()
        window.mainloop()

    def make_window(self):
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
        self.change_values_in_listbox(self._get_tree_view())

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
