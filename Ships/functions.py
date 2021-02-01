from .classes import Ship
from battlefield.classes import Cursor
from config.config import SHIPS_EMPTY_SET
from other.validation import Validation
from random import choice, randint


def new_ship(length, orientation=None, start_point=None):
    if orientation is not None and orientation in ('hor', 'vert'):
        orientation = orientation
    elif orientation is None:
        orientation = choice(('hor', 'vert'))
    else:
        raise ValueError('Orientation must be "hor" or "vert".')

    validation = Validation()
    if start_point is not None:
        validation.check_point_value(start_point)
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


def random_ships_set():
    ships = SHIPS_EMPTY_SET
    validation = Validation()

    all_ships = []
    for length in range(1, 5):
        for ship_idx in ships[length]:

            while True:
                ship = Ship(new_ship(length))
                around_ship = ship.around_ship
                if validation.check_for_matches(all_ships, ship.points):
                    break

            ships[length][ship_idx] = ship
            all_ships += ship.points + around_ship

    return ships
