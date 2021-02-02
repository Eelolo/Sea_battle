from other.validation import Validation
from other.env_vars import load_variable


FIELD_KEYS = load_variable('FIELD_KEYS')
REVERSED = load_variable('REVERSED')


class Battlefield:
    __validation = Validation()

    def new_field(self):
        new_field = {}
        integers = [str(integer) for integer in range(1, 11)]
        letters = [chr(letter) for letter in (range(ord('a'), ord('k')))]
        field_keys = []

        for num in range(10):
            field_keys.append(str(num + 1))
            for idx in range(len(letters)):
                field_keys.append(integers[num] + letters[idx])

        for key in field_keys:
            if 'j' in key:
                new_field[key] = ' ~\n'
            elif len(key) == 1:
                new_field[key] = key + '  '
            elif key == '10':
                new_field[key] = '10 '
            else:
                new_field[key] = ' ~'

        return new_field

    def __init__(self):
        self._field = self.new_field()

    def __setattr__(self, key, value):
        if key == '_field':
            if self.__dict__.get('_field') is not None and value != self.new_field():
                raise ValueError("The field can only be replaced by an identical blank field.")

        self.__dict__[key] = value

    def change_value(self, point: str, value: str):
        self.__validation.check_point_value(point)

        if '\n' in self._field[point]:
            self._field[point] = ' {}\n'.format(value)
        else:
            self._field[point] = ' {}'.format(value)

    def place_ship(self, points: list):
        self.__validation.is_straight_check(points)

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
    __validation = Validation()

    def __init__(self, start_point=None):
        self._field = Battlefield()

        if start_point is not None:
            self.point = start_point
        else:
            self.point = '1a'

        self._field.change_value(self.point, 'X')
        self.__point_key_idx = FIELD_KEYS.index(self.point)

    def __setattr__(self, key, value):
        if key == 'point':
            self.__validation.check_point_value(value)

            if self.__dict__.get('point') is not None:
                self._field.change_value(self.__dict__.get('point'), '~')
                self.__point_key_idx = FIELD_KEYS.index(value)

            self._field.change_value(value, 'X')
        elif key == '_field' and self.__dict__.get('_field') is not None:
            if not isinstance(value, Battlefield):
                raise TypeError('_field attribute must be instance of Battlefield class.')

        self.__dict__[key] = value

    def up(self):
        if self.__point_key_idx not in range(1, 11):
            self.__point_key_idx -= 11
            self.point = FIELD_KEYS[self.__point_key_idx]
        return self.point

    def down(self):
        if self.__point_key_idx not in range(100, 110):
            self.__point_key_idx += 11
            self.point = FIELD_KEYS[self.__point_key_idx]
        return self.point

    def left(self):
        if self.__point_key_idx not in range(1, 111, 11):
            self.__point_key_idx -= 1
            self.point = FIELD_KEYS[self.__point_key_idx]
        return self.point


    def right(self):
        if self.__point_key_idx not in range(10, 110, 11):
            self.__point_key_idx += 1
            self.point = FIELD_KEYS[self.__point_key_idx]
        return self.point

    def move(self, point: str):
        self.__validation.check_point_value(point)
        self.point = point
        return self.point

    def check_method_result(self, method: str):
        self.__validation.check_method(method)

        point = self.point

        getattr(self, method)()

        result = self.point

        if self.point != point:
            getattr(self, REVERSED[method])()

        return result
