from battlefield.classes import Cursor

def check_length(ship, length):
    return len(ship) == length


def is_straight_check(ship):
    if len(ship) == 1:
        return True

    field_keys = Cursor()._field_keys
    for idx in range(len(ship - 1)):
        point_difference = field_keys.index(ship[idx + 1]) - field_keys.index(ship[idx])
        if point_difference not in (1, -1, 11, -11):
            return False

    return True



