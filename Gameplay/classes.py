from battlefield.classes import Battlefield
from ships.functions import random_ships_set


class Player:
    ships = {}

    def define_ship(self):
        pass

    def define_move(self):
        pass


class Opponent:
    ships = {}
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


    def place_ships(self):
        pass

    def realize_move(self):
        pass

    def visualize_player_ships_placing(self):
        pass

    def visualize_playing(self):
        pass
    
    def start(self):
        pass


