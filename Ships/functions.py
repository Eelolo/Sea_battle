from random import choice, randint
from sea_battle.battlefield.classes import Cursor


def new_ship(length, orientation=None, start_point=None):
    if orientation is not None and orientation in ('hor', 'vert'):
        orientation = orientation
    elif orientation is None:
        orientation = choice(('hor', 'vert'))
    else:
        raise ValueError('Orientation must be "hor" or "vert".')

    if start_point is not None:
        if int(start_point[0]) in range(1, 11) and ord(start_point[1]) in range(97, 107):
            if '10' in start_point:
                integer = 10
            else:
                integer = int(start_point[0])
            letter = ord(start_point[1])
    elif start_point is None:
        integer = randint(1, 10)
        letter = randint(97, 106)
        start_point = str(integer) + chr(letter)
    else:
        raise ValueError('Start point must be like "1a" or "6d", in range 1a-10j.')

    ship = []
    cur = Cursor(start_point=start_point)
    ship.append(start_point)
    if orientation == 'hor':
        if letter > 106 - length:
            for _ in range(length - 1):
                ship.append(cur.move('left'))
        else:
            for _ in range(length - 1):
                ship.append(cur.move('right'))
    elif orientation == 'vert':
        if integer > 10 - length:
            for _ in range(length - 1):
                ship.append(cur.move('up'))
        else:
            for _ in range(length - 1):
                ship.append(cur.move('down'))

    return ship
