from random import choice, randint
from battlefield.classes import Cursor
from battlefield.functions import check_point_value
from config.config import SHIPS_EMPTY_SET


def new_ship(length, orientation=None, start_point=None):
    if orientation is not None and orientation in ('hor', 'vert'):
        orientation = orientation
    elif orientation is None:
        orientation = choice(('hor', 'vert'))
    else:
        raise ValueError('Orientation must be "hor" or "vert".')

    if start_point is not None:
        check_point_value(start_point)
        if '10' in start_point:
            integer = 10
        else:
            integer = int(start_point[0])
        letter = ord(start_point[-1])
    else:
        integer = randint(1, 10)
        letter = randint(97, 106)
        start_point = str(integer) + chr(letter)

    ship = []
    cur = Cursor(start_point=start_point)
    ship.append(start_point)
    if orientation == 'hor':
        if letter > 107 - length:
            for _ in range(length - 1):
                ship.append(cur.left())
        else:
            for _ in range(length - 1):
                ship.append(cur.right())
    elif orientation == 'vert':
        if integer > 11 - length:
            for _ in range(length - 1):
                ship.append(cur.up())
        else:
            for _ in range(length - 1):
                ship.append(cur.down())

    return ship


def area_around_ship(ship):
    cur = Cursor()
    length = len(ship)
    if len(ship) == 1:
        point_difference = 1
    else:
        point_difference = cur._field_keys.index(ship[1]) - cur._field_keys.index(ship[0])

    if point_difference in (1, -1):
        if point_difference > 0:
            cur_method = 'right'
        else:
            cur_method = 'left'
    else:
        if point_difference > 0:
            cur_method = 'down'
        else:
            cur_method = 'up'

    around_ship = []
    break_on = None
    for loop_idx in range(3):
        cur.move(ship[0])

        if loop_idx == 0:
            around_ship.append(getattr(cur, cur._reversed_moves[cur_method])())
        else:
            getattr(cur, cur._reversed_moves[cur_method])()
            around_ship.append(getattr(cur, cur._perpendicular_moves[cur_method][loop_idx - 1])())

        if cur.point == ship[0]:
            break_on = length - 1

        for move_idx in range(length + 1):
            around_ship.append(getattr(cur, cur_method)())
            if break_on is not None and move_idx == break_on:
                break

    around_ship = list(set(around_ship) - set(ship))

    return around_ship


def check_for_matches(array0, array1):
    return set(array0) & set(array1) == set()


def random_ships_set():
    ships = SHIPS_EMPTY_SET

    all_ships = []
    for length in range(1, 5):
        for ship_idx in ships[length]:

            while True:
                ship = new_ship(length)
                around_ship = area_around_ship(ship)
                if check_for_matches(all_ships, ship):
                    break

            ships[length][ship_idx][0] = ship
            ships[length][ship_idx][1] = around_ship
            all_ships += ship + around_ship

    return ships
