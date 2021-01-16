from .functions import new_battlefield, check_point_value

class Battlefield:
    def __init__(self):
        self.field = new_battlefield()
        self.amount_ships = 0
        self.ships = []
        self.fourdeck = []
        self.tripledecks = []
        self.doubledecks = []
        self.singledecks = []

    def change_value(self, point, value):
        if '\n' in self.field[point]:
            self.field[point] = ' {}\n'.format(value)
        else:
            self.field[point] = ' {}'.format(value)

    def make_move(self):
        pass

    def __str__(self):
        return '    a b c d e f g h i j\n\n' + \
               ''.join(self.field.values())


class Cursor:
    def __init__(self, start_point=None):
        self._battlefield = Battlefield()
        self._field_keys = list(self._battlefield.field.keys())
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
