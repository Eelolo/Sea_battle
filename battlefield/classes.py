from .functions import new_battlefield, check_point_value
from config.config import REVERSED_MOVES, PERPENDICULAR_MOVES


class Battlefield:
    def __init__(self):
        self._field = new_battlefield()
        self._field_values_to_show = ''.join(self._field.values())

    def __update_field_values(self):
        self._field_values_to_show = ''.join(self._field.values())

    def change_value(self, point, value):
        check_point_value(point)
        if '\n' in self._field[point]:
            self._field[point] = ' {}\n'.format(value)
        else:
            self._field[point] = ' {}'.format(value)
        self.__update_field_values()

    def place_ship(self, ship):
        for point in ship:
            self.change_value(point, '#')

    def make_move(self, point):
        value = '.'
        result = 'Miss.'

        if '#' in self._field[point]:
            value = 'x'
            result = 'Damaged.'

        self.change_value(point, value)
        return result

    def __str__(self):
        return '    a b c d e f g h i j\n\n' + \
               self._field_values_to_show


class Cursor:
    _battlefield = Battlefield()
    _field_keys = list(_battlefield._field.keys())
    _reversed_moves = REVERSED_MOVES
    _perpendicular_moves = PERPENDICULAR_MOVES

    def __init__(self, start_point=None):
        if start_point is not None:
            self.point = start_point
        else:
            self.point = '1a'
        self._battlefield.change_value(self.point, 'X')
        self._point_key_idx = self._field_keys.index(self.point)

    def __setattr__(self, key, value):
        if key == 'point':
            check_point_value(value)
            if self.__dict__.get('point') is not None:
                self._battlefield.change_value(self.__dict__.get('point'), '~')
                self._point_key_idx = self._field_keys.index(value)
            self._battlefield.change_value(value, 'X')

        self.__dict__[key] = value

    def up(self):
        if self._point_key_idx not in range(1, 11):
            self._point_key_idx -= 11
            self.point = self._field_keys[self._point_key_idx]
        return self.point

    def down(self):
        if self._point_key_idx not in range(100, 110):
            self._point_key_idx += 11
            self.point = self._field_keys[self._point_key_idx]
        return self.point

    def left(self):
        if self._point_key_idx not in range(1, 111, 11):
            self._point_key_idx -= 1
            self.point = self._field_keys[self._point_key_idx]
        return self.point


    def right(self):
        if self._point_key_idx not in range(10, 110, 11):
            self._point_key_idx += 1
            self.point = self._field_keys[self._point_key_idx]
        return self.point

    def move(self, point):
        check_point_value(point)
        self.point = point
        return self.point
