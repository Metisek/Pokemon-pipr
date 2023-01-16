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
pokemon1 = GamePokemon(database.get_pokemon_using_pokedex_number(6))
pokemon2 = GamePokemon(database.get_pokemon_using_pokedex_number(27))
pokemon3 = GamePokemon(database.get_pokemon_using_pokedex_number(55))
pokemon4 = GamePokemon(database.get_pokemon_using_pokedex_number(1))


def main():
    run = True
    screen = Screen()
    game = PokemonGame()

    game._set_given_player_pokemon_list([pokemon1, pokemon4], 1)
    game._set_given_player_pokemon_list([pokemon2, pokemon3], 2)

    game.set_game_state('game')
    game.set_menu_state('player_one')
    game.set_real_players_count(2)
    game.game_init_finish()
    game._set_given_player_pokemon_number(2, 2)
    game._set_given_player_pokemon_number(2, 1)
    game.get_exact_object(
        'game', 'player_one', 'player_one_frame').set_active_pokemon(
            game.get_given_player_poke_list(1)[0]
        )
    game.get_exact_object(
        'game', 'player_one', 'player_two_frame').set_active_pokemon(
            game.get_given_player_poke_list(2)[0]
        )
    game.get_exact_object(
        'game', 'player_two', 'player_one_frame').set_active_pokemon(
            game.get_given_player_poke_list(1)[0]
        )
    game.get_exact_object(
        'game', 'player_two', 'player_two_frame').set_active_pokemon(
            game.get_given_player_poke_list(2)[0]
        )

    while run:
        screen.get_clock().tick(FPS)

        # Game widget events
        g_state = game.get_game_state()
        m_state = game.get_menu_state()

        if m_state == 'player_one':
            for special_elem in game.get_object('special_list').get_elem_list():
                if special_elem.raise_event():
                    game.special_pokemon_handle(1)
            for pokemon_elem in game.get_object(
                    'game_pokemon_list').get_elem_list():
                if pokemon_elem.raise_event():
                    game.change_pokemon_handle(
                        pokemon_elem.get_elem_object(), 1)
            if game.raised_event('attack_button'):
                game.attack_pokemon_handle(1)
            elif game.raised_event('special_button'):
                game.get_object('special_list').set_elem_list(
                    game.get_given_player_active_pokemon(1)
                )
                game.get_object('game_pokemon_list').set_is_visible(False)
                game.get_object('special_list').set_is_visible(
                    not game.get_object('special_list').get_is_visible()
                )
            elif game.raised_event('block_button'):
                game.block_pokemon_handle(1)
            elif game.raised_event('change_pokemon_button'):
                game.get_object('game_pokemon_list').set_elem_list(
                    game.get_given_player_poke_list(1)
                )
                game.get_object('special_list').set_is_visible(False)
                game.get_object('game_pokemon_list').set_is_visible(
                    not game.get_object(
                        'game_pokemon_list').get_is_visible()
                )

        elif m_state == 'player_two':
            for pokemon_elem in game.get_object(
                    'game_pokemon_list').get_elem_list():
                if pokemon_elem.raise_event():
                    game.change_pokemon_handle(
                        pokemon_elem.get_elem_object(), 2)
            for special_elem in game.get_object(
                    'special_list').get_elem_list():
                if special_elem.raise_event():
                    game.special_pokemon_handle(2)
            if game.raised_event('attack_button'):
                game.attack_pokemon_handle(2)
            elif game.raised_event('special_button'):
                game.get_object('special_list').set_elem_list(
                    game.get_given_player_active_pokemon(2)
                )
                game.get_object('game_pokemon_list').set_is_visible(False)
                game.get_object('special_list').set_is_visible(
                    not game.get_object('special_list').get_is_visible()
                )
            elif game.raised_event('block_button'):
                game.block_pokemon_handle(2)

            elif game.raised_event('change_pokemon_button'):
                game.get_object('game_pokemon_list').set_elem_list(
                    game.get_given_player_poke_list(2)
                )
                game.get_object('special_list').set_is_visible(False)
                game.get_object('game_pokemon_list').set_is_visible(
                    not game.get_object(
                        'game_pokemon_list').get_is_visible()
                )

        elif m_state == 'pause':
            if game.raised_event('continue_button'):
                game.pause_resume()
            elif game.raised_event('main_menu_button'):
                game.game_reset()
                game.set_game_state('main_menu')
                game.set_menu_state('main_menu')
            elif game.raised_event('quit_button'):
                run = False

        elif m_state == 'finish':
            if game.raised_event('continue_button'):
                game.game_reset()
                game.set_game_state('main_menu')
                game.set_menu_state('main_menu')



        # Game draw static objects

        g_state = game.get_game_state()
        m_state = game.get_menu_state()
        objects = game.get_active_objects()
        screen.draw_bg()

        if m_state == 'player_one':
            pygame.draw.line(screen._get_screen(), (255, 255, 255),
                             (0, 400), (800, 400), 3)
            screen.draw_clear_text((400, 500), "P1")
        elif m_state == 'player_two':
            pygame.draw.line(screen._get_screen(), (255, 255, 255),
                             (0, 400), (800, 400), 3)
            screen.draw_clear_text((400, 500), "P2")
        elif m_state == 'pause':
            screen.draw_clear_text((399, 180), "Pause",
                                   font="BIG_FONT")
        elif m_state == 'finish':
            winner_val = game.get_winner()
            winnet_text = 'Winner: Player {}'.format(
                winner_val if not isinstance
                (winner_val, type(None)) else 'Unknown')

            screen.draw_clear_text((400, 200), winnet_text,
                                   'BIG_FONT')

        screen.draw_objects(objects)
        screen.update_display()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if g_state == 'game':
                        if m_state == 'player_one':
                            game.set_menu_state('pause')
                        elif m_state == 'player_two':
                            game.set_menu_state('pause')
                        elif m_state == 'pause':
                            game.pause_resume()
    pygame.quit()


if __name__ == '__main__':
    main()
