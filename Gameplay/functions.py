from battlefield.classes import Cursor

def check_length(points, length):
    if len(points) != length:
        print('Length must be equal to {}.'.format(length))

        return False

    return True


def is_straight_check(points):
    if len(points) == 1:
        return True
    elif '' in points:
        return False

    field_keys = Cursor()._field_keys
    point_difference = field_keys.index(points[1]) - field_keys.index(points[0])

    if point_difference in (1, -1):
        orientation = 'hor'
    else:
        orientation = 'vert'

    for idx in range(len(points) - 1):
        point_difference = field_keys.index(points[idx + 1]) - field_keys.index(points[idx])

        if orientation == 'hor' and point_difference not in (1, -1) or \
                orientation == 'vert' and point_difference not in (11, -11):
            print('Ship points must be lined up.')

            return False

    return True


def points_on_field_check(points):
    field_keys = set(Cursor()._field_keys) - set(map(lambda x: str(x), range(1, 11)))
    message = 'Entered point not from a field.'

    if len(points) > 1:
        message = message.replace('point', 'points')

    if set(points) - field_keys != set():
        print(message)

        return False

    return True