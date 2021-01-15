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
