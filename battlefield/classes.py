from .functions import new_field
from other.validation import Validation
from config.config import REVERSED, PERPENDICULAR, FIELD_KEYS


class Battlefield:
    validation = Validation()

    def __init__(self):
        self._field = new_field()

    def change_value(self, point: str, value: str):
        self.validation.check_point_value(point)

        if '\n' in self._field[point]:
            self._field[point] = ' {}\n'.format(value)
        else:
            self._field[point] = ' {}'.format(value)

    def place_ship(self, points: list):
        self.validation.is_straight_check(points)

        for point in points:
            self.change_value(point, '#')

    def make_move(self, point: str):
        value = '.'
        result = 'Miss.'

        try:
            if '#' in self._field[point]:
                value = 'x'
                result = 'Damaged.'
            elif 'x' in self._field[point]:
                value = 'x'
        except KeyError:
            pass

        self.change_value(point, value)
        return result

    def __str__(self):
        return '    a b c d e f g h i j\n\n' + \
               ''.join(self._field.values())


class Cursor:
    validation = Validation()

    def __init__(self, start_point=None):
        self._field = Battlefield()

        if start_point is not None:
            self.point = start_point
        else:
            self.point = '1a'

        self._field.change_value(self.point, 'X')
        self._point_key_idx = FIELD_KEYS.index(self.point)

    def __setattr__(self, key, value):
        if key == 'point':
            self.validation.check_point_value(value)

            if self.__dict__.get('point') is not None:
                self._field.change_value(self.__dict__.get('point'), '~')
                self._point_key_idx = FIELD_KEYS.index(value)

            self._field.change_value(value, 'X')

        self.__dict__[key] = value

    def up(self):
        if self._point_key_idx not in range(1, 11):
            self._point_key_idx -= 11
            self.point = FIELD_KEYS[self._point_key_idx]
        return self.point

    def down(self):
        if self._point_key_idx not in range(100, 110):
            self._point_key_idx += 11
            self.point = FIELD_KEYS[self._point_key_idx]
        return self.point

    def left(self):
        if self._point_key_idx not in range(1, 111, 11):
            self._point_key_idx -= 1
            self.point = FIELD_KEYS[self._point_key_idx]
        return self.point


    def right(self):
        if self._point_key_idx not in range(10, 110, 11):
            self._point_key_idx += 1
            self.point = FIELD_KEYS[self._point_key_idx]
        return self.point

    def move(self, point: str):
        self.validation.check_point_value(point)
        self.point = point
        return self.point

    def check_method_result(self, method: str):
        self.validation.check_method(method)

        point = self.point

        getattr(self, method)()

        result = self.point

        if self.point != point:
            getattr(self, REVERSED[method])()

        return result