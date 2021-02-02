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
    __validation = Validation()

    def __init__(self):
        for length in SHIPS_EMPTY_SET:
            for ship_idx in SHIPS_EMPTY_SET[length]:
                ship_attr_name = SHIPS_ATTR_NAMES[length]+str(ship_idx)
                setattr(self, ship_attr_name, None)

    def define_ship(self):
        while True:
            points = input().replace(' ', '').split(',')
            if self.__validation.points_on_field_check(points, message=True):
                break

        return points

    def define_move(self):
        while True:
            point = input()
            if self.__validation.points_on_field_check(point, message=True):
                break

        return point


class Opponent:
    __search_plan = SEARCH_PLAN
    __validation = Validation()

    def _ships_placing(self):
        ships = random_ships_set()

        for length in ships:
            for ship_idx in ships[length]:
                ship_attr_name = SHIPS_ATTR_NAMES[length] + str(ship_idx)
                ship = ships[length][ship_idx]
                setattr(self, ship_attr_name, ship)

    def __init__(self):
        self._status = 'search'
        self._last_move_result = ''
        self._discarded_points = []
        self.__cursor = Cursor()
        self._cur_methods = []
        self._discarded_methods = []
        self._area_to_exclude = []
        self._last_move_point = ''
        self._waits_to_discard = []

        self._ships_placing()

    def __setattr__(self, key, value):
        if key in ('_last_move_result', '_status'):
            if key == '_status':
                values = 'search', 'destruction'
            else:
                values = 'Miss.', 'Damaged.', 'Destroyed.'

            if self.__dict__.get(key) is not None:
                if value not in values:
                    raise ValueError('{} attribute must be in {}.'.format(key, values))

        if key in ('_discarded_points', '_area_to_exclude', '_waits_to_discard', '_last_move_point'):
            if self.__dict__.get(key) is not None:
                self.__validation.points_on_field_check(value)

        if key in ('_cur_methods', '_discarded_methods'):
            if self.__dict__.get(key) is not None:
                if not isinstance(value, list):
                    raise TypeError('{} attribute must be a list that contains methods.'.format(key))

                for method in value:
                    if method not in METHODS:
                        raise ValueError('{} not in {}.'.format(method, METHODS))

        self.__dict__[key] = value

    def _search(self):
        if self.__search_plan:
            while self.__search_plan[-1] in self._discarded_points:
                self.__search_plan.pop(-1)
                if not self.__search_plan:
                    break

        if not self.__search_plan:
            move = self._random_point()
        else:
            move = self.__search_plan.pop(-1)
            self._discarded_points.append(move)

        return move

    def __regulation(self):
        if self._last_move_result == 'Damaged.' and self._cur_methods:
            self._cur_methods.append(self._cur_methods[-1])
            if self.__cursor.check_method_result(self._cur_methods[-1]) in self._discarded_points[:-1]:
                self._last_move_result = 'Miss.'
                self.__cursor.move(self._discarded_points[-1])

        for method in self._cur_methods:
            if self._cur_methods.count(method) >= 2:
                self._discarded_methods.extend(PERPENDICULAR[method])
                if self.__cursor.check_method_result(self._cur_methods[-1]) == self.__cursor.point:
                    self._last_move_result = 'Miss.'
                    self.__cursor.move(self._discarded_points[-1])

        for method in METHODS:
            if self.__cursor.check_method_result(method) in self._discarded_points[:-1]:
                self._discarded_methods.append(method)

        if '1' in self.__cursor.point and '10' not in self.__cursor.point:
            self._discarded_methods.append('up')
        elif '10' in self.__cursor.point:
            self._discarded_methods.append('down')

        if 'a' in self.__cursor.point:
            self._discarded_methods.append('left')
        elif 'j' in self.__cursor.point:
            self._discarded_methods.append('right')

    def __destruction(self):
        if self._last_move_result == 'Damaged.':
            start_point = self._last_move_point
        else:
            start_point = self._discarded_points[-1]

        self.__cursor.move(start_point)

        self.__regulation()

        if not self._cur_methods:
            self._cur_methods.append(
                choice(
                    list(set(METHODS) - set(self._discarded_methods))
                )
            )

        if self._last_move_result == 'Miss.':
            self._cur_methods.append(
                choice(
                    list(set(METHODS) - set(self._cur_methods) - set(self._discarded_methods))
                )
            )

        method = self._cur_methods[-1]
        move = getattr(self.__cursor, method)()
        self._waits_to_discard.append(move)

        return move

    def _random_point(self):
        nums_set = {str(num) for num in range(1, 11)}
        available_points = list(set(FIELD_KEYS) - nums_set - set(self._discarded_points))
        move = choice(available_points)
        self._discarded_points.append(move)
        return move

    def _define_move(self):
        if self._last_move_result == 'Damaged.':
            self._status = 'destruction'
        elif self._last_move_result == 'Destroyed.':
            self._cur_methods = []
            self._discarded_methods = []
            self._discarded_points += self._area_to_exclude + self._waits_to_discard
            self._waits_to_discard = []
            self._status = 'search'

        if self._status == 'destruction':
            move = self.__destruction()
        else:
            move = self._search()

        return move


class Game:
    __validation = Validation()

    def __init__(self):
        self._player_field = Battlefield()
        self._opponent_field = Battlefield()
        self._hidden_field = Battlefield()
        self._player = Player()
        self._opponent = Opponent()

    def __setattr__(self, key, value):
        attrs = ['_player_field', '_opponent_field', '_hidden_field', '_player', '_opponent']
        if key in attrs:
            if self.__dict__.get(key) is not None:
                instance = self.__dict__.get(key)
                if not isinstance(value, type(instance)):
                    raise TypeError(
                        '{} attribute must be instance of {} class.'. format(
                            key, type(instance).__name__
                        )
                    )

        self.__dict__[key] = value

    def _player_ships_placing(self):
        all_ships = []
        for length in SHIPS_EMPTY_SET:
            for ship_idx in SHIPS_EMPTY_SET[length]:

                os.system('cls')
                # os.system('clear')
                print(FIELD.format(self._player_field))
                print(EXPLANATIONS[SHIPS_ATTR_NAMES[length]])

                while True:
                    points = self._player.define_ship()

                    if False not in (
                            self.__validation.check_for_matches(all_ships, points, message=True),
                            self.__validation.check_length(points, length),
                            self.__validation.is_straight_check(points, message=True)
                    ):
                        ship = Ship(points)
                        break

                around_ship = ship.around_ship

                ship_attr_name = SHIPS_ATTR_NAMES[length]+str(ship_idx)
                setattr(self._player, ship_attr_name, ship)

                self._player_field.place_ship(ship._points)

                all_ships += ship._points + around_ship

    def _opponent_ships_placing(self):
        ships = SHIPS_EMPTY_SET

        for length in ships:
            for ship_idx in ships[length]:
                ship_attr_name = SHIPS_ATTR_NAMES[length]+str(ship_idx)
                points = getattr(self._opponent, ship_attr_name)._points

                self._opponent_field.place_ship(points)

    def __is_destroyed_check(self, move, player):
        ships = SHIPS_EMPTY_SET
        field = getattr(self, player + '_field')._field
        player_object = getattr(self, player)

        around_ship = None
        for length in range(1, 5):
            for ship_idx in ships[length]:
                ship_attr_name = SHIPS_ATTR_NAMES[length]+str(ship_idx)
                ship = getattr(player_object, ship_attr_name)
                if move in ship._points:
                    around_ship = ship.around_ship
                    break
            else:
                continue
            break

        if around_ship:
            field_values = ''.join([field[point] for point in ship._points])
            if '#' not in field_values and ship.destroyed == False:
                return around_ship, player_object, ship_attr_name

    def __outline_ship(self, move, field_name, player):
        check_result = self.__is_destroyed_check(move, player)

        if check_result:
            ship_object = getattr(check_result[1], check_result[2])
            setattr(ship_object, 'destroyed', True)

            around_ship = check_result[0]
            result = 'Destroyed.'
            for point in around_ship:
                getattr(self, field_name).change_value(point, '.')

            return result, around_ship

    def _player_move(self):
        move = self._player.define_move()
        result = self._opponent_field.make_move(move)
        is_destroyed = self.__outline_ship(move, '_opponent_field', '_opponent')

        if is_destroyed:
            result = is_destroyed[0]

        for key in self._opponent_field._field:
            if self._hidden_field._field[key] != self._opponent_field._field[key]:
                if 'x' in self._opponent_field._field[key]:
                    self._hidden_field.change_value(key, 'x')
                elif '.' in self._opponent_field._field[key]:
                    self._hidden_field.change_value(key, '.')

        return result

    def _opponent_move(self):
        move = self._opponent._define_move()
        self._opponent._last_move_point = move
        self._opponent._last_move_result = self._player_field.make_move(move)
        is_destroyed = self.__outline_ship(move, '_player_field', '_player')

        if is_destroyed:
            self._opponent._last_move_result = is_destroyed[0]
            self._opponent._area_to_exclude = is_destroyed[1]

        time.sleep(1.0)

        return move, self._opponent._last_move_result

    def __print_fields(self, player_result):
        if self._opponent._last_move_point:
            opp_info = 'Opponent`s move: {}. {}'.format(
                self._opponent._last_move_point, self._opponent._last_move_result
            )
        else:
            opp_info = ''

        if not player_result:
            player_result = ''

        os.system('cls')
        # os.system('clear')
        print(
            GAME.format(
                self._player_field, opp_info, self._hidden_field, player_result
            )
        )

    def __repeat_move(self, player, player_result=None):
        if player == 'player':
            result = player_result
        else:
            result = self._opponent._last_move_result

        while result in ('Damaged.', 'Destroyed.'):
            if player == 'player':
                result = self._player_move()
            else:
                self._opponent_move()
                result = self._opponent._last_move_result

            self.__print_fields(player_result)
            self.__end_check()

        if player == 'player':
            return result

    def __end(self, player):
        if player == 'player':
            message = '        You won!'
        else:
            message = '         Defeat.'

        print(message)

        exit()

    def __end_check(self):
        if '#' not in str(self._player_field):
            self.__end('opponent')
        elif '#' not in str(self._opponent_field):
            self.__end('player')

    def _game(self):
        player_result = ''

        self.__print_fields(player_result)
        while True:
            player_result = self._player_move()
            self.__print_fields(player_result)
            self.__end_check()
            player_result = self.__repeat_move('player', player_result)

            self._opponent_move()
            self.__print_fields(player_result)
            self.__end_check()
            self.__repeat_move('opponent')

    def start(self):
        self._player_ships_placing()
        self._opponent_ships_placing()
        self._game()
