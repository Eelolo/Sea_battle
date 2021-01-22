from battlefield.classes import Battlefield
from ships.classes import Ship
from ships.functions import random_ships_set, check_for_matches
from config.config import SHIPS_EMPTY_SET
from config.templates.defining_ships import BATTLEFIELD, EXPLANATIONS
from .functions import check_length, is_straight_check, points_in_field_keys_check
import os


class Player:
    ships = SHIPS_EMPTY_SET

    def define_ship(self):
        ship = input().replace(' ', '').split(',')
        return ship

    def define_move(self):
        move = input()
        return move


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
                    ship = Ship(self.player.define_ship())
                    if not check_for_matches(all_ships, ship):
                        print('Ship is too close to another.')
                    if False not in (
                            check_for_matches(all_ships, ship),
                            points_in_field_keys_check(ship),
                            check_length(ship, length),
                            is_straight_check(ship)
                    ):
                        break

                around_ship = ship.around_ship
                self.player.ships[length][ship_idx] = ship
                self.player_battlefield.place_ship(ship.ship)

                all_ships += ship.ship + around_ship

    def opponent_ships_placing(self):
        ships = self.opponent.ships

        for length in range(1, 5):
            for ship_idx in ships[length]:
                self.opponent_battlefield.place_ship(ships[length][ship_idx].ship)

    def is_destroyed_check(self, move, player):
        ships = getattr(self, player).ships
        field = getattr(self, player + '_battlefield')._field

        ship = []
        for length in range(1, 5):
            for ship_idx in ships[length]:
                if move in ships[length][ship_idx].ship:
                    ship = ships[length][ship_idx]
                    around_ship = ship.around_ship
                    break
            else:
                continue
            break

        if ship:
            values = ''.join([field[point] for point in ship.ship])
            if '#' not in values:
                return around_ship

    def outline_ship(self, move, field_name, player):
        around_ship = self.is_destroyed_check(move, player)

        if around_ship:
            result = 'Destroyed.'
            for point in around_ship:
                getattr(self, field_name).change_value(point, '.')

            return result

    def player_move(self):
        move = self.player.define_move()
        result = self.opponent_battlefield.make_move(move)
        is_destroyed = self.outline_ship(move, 'opponent_battlefield', 'opponent')

        if is_destroyed:
            result = is_destroyed

        return result

    def opponent_move(self):
        move = self.opponent.define_move()
        self.opponent.last_move = self.player_battlefield.make_move(move)
        is_destroyed = self.outline_ship(move, 'player_battlefield', 'player')

        if is_destroyed:
            self.opponent.last_move = is_destroyed

        return  self.opponent.last_move

    def visualize_playing(self):
        os.system('cls')
        # os.system('clear'
        print(self.opponent_battlefield)
        while True:
            result = self.player_move()
            os.system('cls')
            # os.system('clear')
            print(self.opponent_battlefield)
            print(result)



    
    def start(self):
        # self.__player_ships_placing()
        self.opponent_ships_placing()
        self.visualize_playing()
