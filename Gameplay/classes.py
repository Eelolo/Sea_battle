from battlefield.classes import Battlefield
from ships.functions import random_ships_set, area_around_ship, check_for_matches
from config.config import SHIPS_EMPTY_SET
from config.templates.defining_ships import BATTLEFIELD, EXPLANATIONS
import os


class Player:
    ships = SHIPS_EMPTY_SET

    def define_ship(self):
        ship = input()
        return ship

    def define_move(self):
        pass


class Opponent:
    played_moves = []
    last_move = ''
    last_move_is_damaged = bool

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
    
    def place_ships(self):
        pass

    def realize_move(self):
        pass

    def player_ships_placing(self):

        all_ships = []
        for length_idx, length in enumerate(self.player.ships):
            for ship_idx in self.player.ships[length]:

                os.system('cls')
                # os.system('clear')
                print(BATTLEFIELD.format(''.join(self.player_battlefield.field.values())))
                print(EXPLANATIONS[list(EXPLANATIONS.keys())[length_idx]])

                while True:
                    ship = self.player.define_ship().split(',')
                    around_ship = area_around_ship(ship)
                    if check_for_matches(all_ships, ship):
                        break
                    print('корабль слишком близко к другому')

                self.player.ships[length][ship_idx][0] = ship
                self.player.ships[length][ship_idx][1] = around_ship

                for point in ship:
                    self.player_battlefield.change_value(point, '#')

                all_ships += ship + around_ship

    def visualize_playing(self):
        pass
    
    def start(self):
        pass
