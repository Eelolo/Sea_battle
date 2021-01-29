from battlefield.classes import Cursor

def check_length(ship, length):
    if len(ship) != length:
        print('Length must be equal to {}.'.format(length))

        return False

    return True


def is_straight_check(ship):
    if len(ship) == 1:
        return True
    elif '' in ship:
        return False

    field_keys = Cursor()._field_keys
    point_difference = field_keys.index(ship[1]) - field_keys.index(ship[0])

    if point_difference in (1, -1):
        orientation = 'hor'
    else:
        orientation = 'vert'

    for idx in range(len(ship) - 1):
        point_difference = field_keys.index(ship[idx + 1]) - field_keys.index(ship[idx])

        if orientation == 'hor' and point_difference not in (1, -1) or \
                orientation == 'vert' and point_difference not in (11, -11):
            print('Ship points must be lined up.')

            return False

    return True

def points_in_field_keys_check(ship):
    field_keys = set(Cursor()._field_keys) - set(map(lambda x: str(x), range(1, 11)))

    if set(ship) - field_keys != set():
        print('Entered points not from a field.')

        return False

    return True

def point_in_field_keys_check(point):
    field_keys = set(Cursor()._field_keys) - set(map(lambda x: str(x), range(1, 11)))

    if point not in field_keys:
        print('Entered point not from a field.')

        return False

    return True