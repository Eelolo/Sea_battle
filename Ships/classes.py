from .functions import area_around_ship
from battlefield.classes import Cursor


class Ship:
    def point_difference(self, ship):
        cur = Cursor()
        point_difference = cur._field_keys.index(ship[1]) - cur._field_keys.index(ship[0])

        return point_difference

    def define_orientation(self):
        if self.point_difference in (1, -1):
            orientation = 'hor'
        else:
            orientation = 'vert'

        return orientation

    def __init__(self, ship, around_ship=None):
        self.length = len(ship)
        self._point_difference = self.point_difference(ship)
        self.orientation = self.define_orientation()
        self.ship = ship

        if around_ship is not None:
            self.around_ship = around_ship
        else:
            self.around_ship = area_around_ship(ship)

        self.destroyed = False

    def __str__(self):
        cur = Cursor()
        cur._battlefield.place_ship(self.ship)

        return '    a b c d e f g h i j\n\n' + \
               cur._battlefield._field_values_to_show
