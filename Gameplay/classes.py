from battlefield.classes import Battlefield, Cursor
from ships.classes import Ship
from ships.functions import random_ships_set, check_for_matches
from config.config import (
    SHIPS_EMPTY_SET, SHIPS_ATTR_NAMES, METHODS, REVERSED_MOVES, PERPENDICULAR_MOVES, SEARCH_PLAN
)
from config.templates.defining_ships import BATTLEFIELD, EXPLANATIONS
from .functions import check_length, is_straight_check, points_in_field_keys_check
from random import choice
import os
import time


class Player:
    def __init__(self):
        for length in SHIPS_EMPTY_SET:
            for ship_idx in SHIPS_EMPTY_SET[length]:
                ship_attr_name = SHIPS_ATTR_NAMES[length]+str(ship_idx)
                setattr(self, ship_attr_name, None)

    def define_ship(self):
        ship = input().replace(' ', '').split(',')
        return ship

    def define_move(self):
        move = input()
        return move


class Opponent:
    search_plan = SEARCH_PLAN

    def ships_placing(self):
        ships = random_ships_set()

        for length in ships:
            for ship_idx in ships[length]:
                ship_attr_name = SHIPS_ATTR_NAMES[length] + str(ship_idx)
                ship = ships[length][ship_idx]
                setattr(self, ship_attr_name, ship)

    def __init__(self):
        self.status = 'search'
        self.last_move_result = ''
        self.discarded_points = []
        self.cursor = Cursor()
        self.cur_methods = []
        self.discarded_methods = []
        self.area_to_exclude = []
        self.last_move_point = ''
        self.waits_to_discard = []

        self.ships_placing()

    def search(self):
        if self.search_plan:
            while self.search_plan[-1] in self.discarded_points:
                self.search_plan.pop(-1)
                if not self.search_plan:
                    break

        if not self.search_plan:
            move = self.random_point()
        else:
            move = self.search_plan.pop(-1)
            self.discarded_points.append(move)

        return move

    def regulation(self):
        if self.last_move_result == 'Damaged.' and self.cur_methods:
            self.cur_methods.append(self.cur_methods[-1])

        for method in self.cur_methods:
            if self.cur_methods.count(method) >= 2:
                self.discarded_methods.extend(PERPENDICULAR_MOVES[method])
                if self.cursor.check_move_result(self.cur_methods[-1]) == self.cursor.point:
                    self.last_move_result = 'Miss.'
                    self.cursor.move(self.discarded_points[-1])

        for method in METHODS:
            if self.cursor.check_move_result(method) in self.discarded_points[:-1]:
                self.discarded_methods.append(method)

        if '1' in self.cursor.point and '10' not in self.cursor.point:
            self.discarded_methods.append('up')
        elif '10' in self.cursor.point:
            self.discarded_methods.append('down')

        if 'a' in self.cursor.point:
            self.discarded_methods.append('left')
        elif 'j' in self.cursor.point:
            self.discarded_methods.append('right')

    def destruction(self):
        if self.last_move_result == 'Damaged.':
            start_point = self.last_move_point
        else:
            start_point = self.discarded_points[-1]

        self.cursor.move(start_point)

        self.regulation()

        if not self.cur_methods:
            self.cur_methods.append(
                choice(
                    list(set(METHODS) - set(self.discarded_methods))
                )
            )

        if self.last_move_result == 'Miss.':
            self.cur_methods.append(
                choice(
                    list(set(METHODS) - set(self.cur_methods) - set(self.discarded_methods))
                )
            )

        method = self.cur_methods[-1]
        move = getattr(self.cursor, method)()
        self.waits_to_discard.append(move)

        return move

    def random_point(self):
        cur = Cursor()
        nums_set = {str(num) for num in range(1, 11)}
        available_points = list(set(cur._field_keys) - nums_set - set(self.discarded_points))
        move = choice(available_points)
        self.discarded_points.append(move)
        return move

    def define_move(self):
        if self.last_move_result == 'Damaged.':
            self.status = 'destruction'
        elif self.last_move_result == 'Destroyed.':
            self.cur_methods = []
            self.discarded_methods = []
            self.discarded_points += self.area_to_exclude + self.waits_to_discard
            self.waits_to_discard = []
            self.status = 'search'

        if self.status == 'destruction':
            move = self.destruction()
        else:
            move = self.search()

        return move


class Game:
    def __init__(self):
        self.player_battlefield = Battlefield()
        self.opponent_battlefield = Battlefield()
        self.player = Player()
        self.opponent = Opponent()
        self.start()

    def __player_ships_placing(self):
        all_ships = []
        for length_idx, length in enumerate(SHIPS_EMPTY_SET):
            for ship_idx in SHIPS_EMPTY_SET[length]:

                os.system('cls')
                # os.system('clear')
                print(BATTLEFIELD.format(self.player_battlefield._field_values_to_show))
                print(EXPLANATIONS[length_idx])

                while True:
                    ship = Ship(self.player.define_ship())
                    if not check_for_matches(all_ships, ship.ship):
                        print('Ship is too close to another.')
                    if False not in (
                            check_for_matches(all_ships, ship.ship),
                            points_in_field_keys_check(ship.ship),
                            check_length(ship.ship, length),
                            is_straight_check(ship.ship)
                    ):
                        break

                around_ship = ship.around_ship

                ship_attr_name = SHIPS_ATTR_NAMES[length]+str(ship_idx)
                setattr(self.player, ship_attr_name, ship)

                self.player_battlefield.place_ship(ship.ship)

                all_ships += ship.ship + around_ship

    def opponent_ships_placing(self):
        ships = SHIPS_EMPTY_SET

        for length in ships:
            for ship_idx in ships[length]:
                ship_attr_name = SHIPS_ATTR_NAMES[length]+str(ship_idx)
                ship = getattr(self.opponent, ship_attr_name).ship

                self.opponent_battlefield.place_ship(ship)

    def is_destroyed_check(self, move, player):
        ships = SHIPS_EMPTY_SET
        field = getattr(self, player + '_battlefield')._field
        player_object = getattr(self, player)

        around_ship = None
        for length in range(1, 5):
            for ship_idx in ships[length]:
                ship_attr_name = SHIPS_ATTR_NAMES[length]+str(ship_idx)
                ship = getattr(player_object, ship_attr_name)
                if move in ship.ship:
                    around_ship = ship.around_ship
                    break
            else:
                continue
            break

        if around_ship:
            field_values = ''.join([field[point] for point in ship.ship])
            if '#' not in field_values and ship.destroyed == False:
                return around_ship, player_object, ship_attr_name

    def outline_ship(self, move, field_name, player):
        check_result = self.is_destroyed_check(move, player)

        if check_result:
            ship_object = getattr(check_result[1], check_result[2])
            setattr(ship_object, 'destroyed', True)

            around_ship = check_result[0]
            result = 'Destroyed.'
            for point in around_ship:
                getattr(self, field_name).change_value(point, '.')

            return result, around_ship

    def player_move(self):
        move = self.player.define_move()
        result = self.opponent_battlefield.make_move(move)
        is_destroyed = self.outline_ship(move, 'opponent_battlefield', 'opponent')

        if is_destroyed:
            result = is_destroyed[0]

        return result

    def opponent_move(self):
        move = self.opponent.define_move()
        self.opponent.last_move_point = move
        self.opponent.last_move_result = self.player_battlefield.make_move(move)
        is_destroyed = self.outline_ship(move, 'player_battlefield', 'player')

        if is_destroyed:
            self.opponent.last_move_result = is_destroyed[0]
            self.opponent.area_to_exclude = is_destroyed[1]

        return self.opponent.last_move_result

    def game(self):
        os.system('cls')
        # os.system('clear')
        print(self.player_battlefield)
        while True:
            # input()
            time.sleep(1.0)
            result = self.opponent_move()
            print(result)
            os.system('cls')
            # os.system('clear')
            print(self.player_battlefield)

    def start(self):
        # self.__player_ships_placing()
        ships = random_ships_set()

        for length in ships:
            for ship_idx in ships[length]:
                ship_attr_name = SHIPS_ATTR_NAMES[length] + str(ship_idx)
                ship = ships[length][ship_idx]
                setattr(self.player, ship_attr_name, ship)

                self.player_battlefield.place_ship(ship.ship)

        self.opponent_ships_placing()
        self.game()
