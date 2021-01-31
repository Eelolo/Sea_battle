from battlefield.classes import Battlefield, Cursor
from config.config import SHIPS_EMPTY_SET, SHIPS_ATTR_NAMES, SEARCH_PLAN
from config.templates.defining_ships import FIELD, EXPLANATIONS
from config.templates.game import GAME
from other.validation import Validation
from other.env_vars import load_variable
from random import choice
from ships.classes import Ship
from ships.functions import random_ships_set
import os
import time


FIELD_KEYS = load_variable('FIELD_KEYS')
METHODS = load_variable('METHODS')
PERPENDICULAR = load_variable('PERPENDICULAR')


class Player:
    validation = Validation()

    def __init__(self):
        for length in SHIPS_EMPTY_SET:
            for ship_idx in SHIPS_EMPTY_SET[length]:
                ship_attr_name = SHIPS_ATTR_NAMES[length]+str(ship_idx)
                setattr(self, ship_attr_name, None)

    def define_ship(self):
        while True:
            points = input().replace(' ', '').split(',')
            if self.validation.points_on_field_check(points, message=True):
                break

        return points

    def define_move(self):
        while True:
            point = input()
            if self.validation.points_on_field_check(point, message=True):
                break

        return point


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
            if self.cursor.check_method_result(self.cur_methods[-1]) in self.discarded_points[:-1]:
                self.last_move_result = 'Miss.'
                self.cursor.move(self.discarded_points[-1])

        for method in self.cur_methods:
            if self.cur_methods.count(method) >= 2:
                self.discarded_methods.extend(PERPENDICULAR[method])
                if self.cursor.check_method_result(self.cur_methods[-1]) == self.cursor.point:
                    self.last_move_result = 'Miss.'
                    self.cursor.move(self.discarded_points[-1])

        for method in METHODS:
            if self.cursor.check_method_result(method) in self.discarded_points[:-1]:
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
        nums_set = {str(num) for num in range(1, 11)}
        available_points = list(set(FIELD_KEYS) - nums_set - set(self.discarded_points))
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
    validation = Validation()

    def __init__(self):
        self.player_field = Battlefield()
        self.opponent_field = Battlefield()
        self.hidden_field = Battlefield()
        self.player = Player()
        self.opponent = Opponent()
        self.start()

    def __player_ships_placing(self):
        all_ships = []
        for length in SHIPS_EMPTY_SET:
            for ship_idx in SHIPS_EMPTY_SET[length]:

                os.system('cls')
                # os.system('clear')
                print(FIELD.format(self.player_field))
                print(EXPLANATIONS[SHIPS_ATTR_NAMES[length]])

                while True:
                    points = self.player.define_ship()

                    if False not in (
                            self.validation.check_for_matches(all_ships, points, message=True),
                            self.validation.check_length(points, length),
                            self.validation.is_straight_check(points, message=True)
                    ):
                        ship = Ship(points)
                        break

                around_ship = ship.around_ship

                ship_attr_name = SHIPS_ATTR_NAMES[length]+str(ship_idx)
                setattr(self.player, ship_attr_name, ship)

                self.player_field.place_ship(ship.points)

                all_ships += ship.points + around_ship

    def opponent_ships_placing(self):
        ships = SHIPS_EMPTY_SET

        for length in ships:
            for ship_idx in ships[length]:
                ship_attr_name = SHIPS_ATTR_NAMES[length]+str(ship_idx)
                points = getattr(self.opponent, ship_attr_name).points

                self.opponent_field.place_ship(points)

    def is_destroyed_check(self, move, player):
        ships = SHIPS_EMPTY_SET
        field = getattr(self, player + '_field')._field
        player_object = getattr(self, player)

        around_ship = None
        for length in range(1, 5):
            for ship_idx in ships[length]:
                ship_attr_name = SHIPS_ATTR_NAMES[length]+str(ship_idx)
                ship = getattr(player_object, ship_attr_name)
                if move in ship.points:
                    around_ship = ship.around_ship
                    break
            else:
                continue
            break

        if around_ship:
            field_values = ''.join([field[point] for point in ship.points])
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
        result = self.opponent_field.make_move(move)
        is_destroyed = self.outline_ship(move, 'opponent_field', 'opponent')

        if is_destroyed:
            result = is_destroyed[0]

        for key in self.opponent_field._field:
            if self.hidden_field._field[key] != self.opponent_field._field[key]:
                if 'x' in self.opponent_field._field[key]:
                    self.hidden_field.change_value(key, 'x')
                elif '.' in self.opponent_field._field[key]:
                    self.hidden_field.change_value(key, '.')

        return result

    def opponent_move(self):
        move = self.opponent.define_move()
        self.opponent.last_move_point = move
        self.opponent.last_move_result = self.player_field.make_move(move)
        is_destroyed = self.outline_ship(move, 'player_field', 'player')

        if is_destroyed:
            self.opponent.last_move_result = is_destroyed[0]
            self.opponent.area_to_exclude = is_destroyed[1]

        time.sleep(1.0)

        return move, self.opponent.last_move_result

    def print_fields(self, player_result):
        if self.opponent.last_move_point:
            opp_info = 'Opponent`s move: {}. {}'.format(
                self.opponent.last_move_point, self.opponent.last_move_result
            )
        else:
            opp_info = ''

        if not player_result:
            player_result = ''

        os.system('cls')
        # os.system('clear')
        print(
            GAME.format(
                self.player_field, opp_info, self.hidden_field, player_result
            )
        )

    def repeat_move(self, player, player_result=None):
        if player == 'player':
            result = player_result
        else:
            result = self.opponent.last_move_result

        while result in ('Damaged.', 'Destroyed.'):
            if player == 'player':
                result = self.player_move()
            else:
                self.opponent_move()
                result = self.opponent.last_move_result

            self.print_fields(player_result)
            self.end_check()

        if player == 'player':
            return result

    def end(self, player):
        if player == 'player':
            message = '        You won!'
        else:
            message = '         Defeat.'

        print(message)

        exit()

    def end_check(self):
        if '#' not in str(self.player_field):
            self.end('opponent')
        elif '#' not in str(self.opponent_field):
            self.end('player')

    def game(self):
        player_result = ''

        self.print_fields(player_result)
        while True:
            player_result = self.player_move()
            self.print_fields(player_result)
            self.end_check()
            player_result = self.repeat_move('player', player_result)

            self.opponent_move()
            self.print_fields(player_result)
            self.end_check()
            self.repeat_move('opponent')

    def start(self):
        self.__player_ships_placing()
        self.opponent_ships_placing()
        self.game()
