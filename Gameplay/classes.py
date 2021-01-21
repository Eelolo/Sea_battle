from battlefield.classes import Battlefield
from ships.functions import random_ships_set, area_around_ship, check_for_matches
from config.config import SHIPS_EMPTY_SET
from config.templates.defining_ships import BATTLEFIELD, EXPLANATIONS
from .functions import check_length, is_straight_check, points_in_field_keys_check, is_destroyed_check
import os


class Player:
    ships = SHIPS_EMPTY_SET

    def define_ship(self):
        ship = input().replace(' ', '').split(',')
        return ship

    def define_move(self):
        pass


class Opponent:
    played_moves = []
    last_move = ''

    def __init__(self):
        self.ships = random_ships_set()

    def define_move(self):
        pass


class Game:
    player_battlefield = Battlefield()
    opponent_battlefield = Battlefield()
    player = Player()
    opponent = Opponent()

    def __init__(self):
        self.start()

    def __player_ships_placing(self):
        all_ships = []
        for length_idx, length in enumerate(self.player.ships):
            for ship_idx in self.player.ships[length]:

                os.system('cls')
                # os.system('clear')
                print(BATTLEFIELD.format(self.player_battlefield._field_values_to_show))
                print(EXPLANATIONS[length_idx])

                while True:
                    ship = self.player.define_ship()
                    if not check_for_matches(all_ships, ship):
                        print('Ship is too close to another.')
                    if False not in (
                            check_for_matches(all_ships, ship),
                            points_in_field_keys_check(ship),
                            check_length(ship, length),
                            is_straight_check(ship)
                    ):
                        break

                around_ship = area_around_ship(ship)

                self.player.ships[length][ship_idx][0] = ship
                self.player.ships[length][ship_idx][1] = around_ship

                self.player_battlefield.place_ship(ship)

                all_ships += ship + around_ship

    def outline_ship(self, move, field_name):
        around_ship = is_destroyed_check(move)

        if around_ship:
            result = 'Destroyed.'
            for point in around_ship:
                getattr(self, field_name).change_value(point, '.')

            return result

    def player_move(self):
        move = self.player.define_move()
        result = self.opponent_battlefield.make_move(move)
        is_destroyed = self.outline_ship(move, 'opponent_battlefield')

        if is_destroyed:
            result = is_destroyed

        print(result)

    def opponent_move(self):
        move = self.opponent.define_move()
        self.opponent.last_move = self.player_battlefield.make_move(move)
        is_destroyed = self.outline_ship(move, 'player_battlefield')

        if is_destroyed:
            self.opponent.last_move = is_destroyed

        print(self.opponent.last_move)

    def visualize_playing(self):
        pass
    
    def start(self):
        self.__player_ships_placing()
