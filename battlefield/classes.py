from .functions import new_battlefield

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
        self.battlefield = Battlefield()
        self.field_keys = list(self.battlefield.field.keys())
        if start_point is not None:
            self.point = start_point
        else:
            self.point = '1a'
        self.battlefield.change_value(self.point, 'X')
        self.point_key_idx = self.field_keys.index(self.point)

    def up(self):
        if self.point_key_idx not in range(1, 11):
            self.point_key_idx -= 11
            self.point = self.field_keys[self.point_key_idx]
        return self.point

    def down(self):
        if self.point_key_idx not in range(100, 110):
            self.point_key_idx += 11
            self.point = self.field_keys[self.point_key_idx]
        return self.point

    def left(self):
        if self.point_key_idx not in range(1, 111, 11):
            self.point_key_idx -= 1
            self.point = self.field_keys[self.point_key_idx]
        return self.point


    def right(self):
        if self.point_key_idx not in range(10, 110, 11):
            self.point_key_idx += 1
            self.point = self.field_keys[self.point_key_idx]
        return self.point

    def move(self, move):
        if move in ('up', 'down', 'left', 'right'):
            self.battlefield.change_value(self.point, '~')
            new_point = getattr(self, move)()
            self.battlefield.change_value(new_point, 'X')
        else:
            raise ValueError('Move must be in: up, down, left, right.')

        return new_point