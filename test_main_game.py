import pygame
# from pygame_objects import Button, PokemonList, PokemonListElem, PokemonBalls
from attributes import (
    FPS,
)

from main import PokemonGame, Screen, TkPokemonSelectWindow, TextDatabase

# from classes import (
#     RedundantKeyError
# )

from classes import GamePokemon
from database import PokemonDatabase

database = PokemonDatabase('pokemon.json')
pokemon1 = GamePokemon(database.get_pokemon_using_pokedex_number(3))
pokemon2 = GamePokemon(database.get_pokemon_using_pokedex_number(30))


def main():
    run = True
    screen = Screen()
    game = PokemonGame()

    game._set_given_player_pokemon_list([pokemon1], 1)
    game._set_given_player_pokemon_list([pokemon2], 2)

    game.set_game_state('game')
    game.set_menu_state('player_one')
    game.set_real_players_count(2)
    game.draw_starting_turn()
    game.get_exact_object(
        'game', 'player_one', 'player_one_frame').set_active_pokemon(
            game.get_given_player_pokemon_list(1)[0]
        )
    game.get_exact_object(
        'game', 'player_one', 'player_two_frame').set_active_pokemon(
            game.get_given_player_pokemon_list(2)[0]
        )
    game.get_exact_object(
        'game', 'player_two', 'player_one_frame').set_active_pokemon(
            game.get_given_player_pokemon_list(1)[0]
        )
    game.get_exact_object(
        'game', 'player_two', 'player_two_frame').set_active_pokemon(
            game.get_given_player_pokemon_list(2)[0]
        )

    while run:
        screen.get_clock().tick(FPS)

        # Game widget events
        g_state = game.get_game_state()
        m_state = game.get_menu_state()

        if m_state == 'player_one':
            pass

        elif m_state == 'player_two':
            pass

        # Game draw static objects

        g_state = game.get_game_state()
        m_state = game.get_menu_state()
        objects = game.get_active_objects()
        screen.draw_bg()

        if m_state == 'player_one':
            pygame.draw.line(screen._get_screen(), (255, 255, 255),
                             (0, 400), (800, 400), 3)
        elif m_state == 'player_two':
            pygame.draw.line(screen._get_screen(), (255, 255, 255),
                             (0, 400), (800, 400), 3)
        elif m_state == 'pause':
            pass

        screen.draw_objects(objects)
        screen.update_display()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()


if __name__ == '__main__':
    main()
