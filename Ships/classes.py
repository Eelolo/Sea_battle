from battlefield.classes import Cursor


class Ship:
    def point_difference(self, ship):
        cur = Cursor()
        if len(ship) == 1:
            point_difference = 1
        else:
            point_difference = cur._field_keys.index(ship[1]) - cur._field_keys.index(ship[0])

        return point_difference

    def define_orientation(self):
        if self.point_difference in (1, -1):
            orientation = 'hor'
        else:
            orientation = 'vert'

        return orientation

    def area_around_ship(self, ship):
        if self.point_difference in (1, -1):
            if self.point_difference > 0:
                cur_method = 'right'
            else:
                cur_method = 'left'
        else:
            if self.point_difference > 0:
                cur_method = 'down'
            else:
                cur_method = 'up'

        cur = Cursor()
        around_ship = []
        break_on = None
        for loop_idx in range(3):
            cur.move(ship[0])

            if loop_idx == 0:
                around_ship.append(getattr(cur, cur._reversed_moves[cur_method])())
            else:
                getattr(cur, cur._reversed_moves[cur_method])()
                around_ship.append(getattr(cur, cur._perpendicular_moves[cur_method][loop_idx - 1])())

            if cur.point == ship[0]:
                break_on = self.length - 1

            for move_idx in range(self.length + 1):
                around_ship.append(getattr(cur, cur_method)())
                if break_on is not None and move_idx == break_on:
                    break

        around_ship = list(set(around_ship) - set(ship))

        return around_ship

    def __init__(self, ship, around_ship=None):
        self.length = len(ship)
        self.point_difference = self.point_difference(ship)
        self.orientation = self.define_orientation()
        self.ship = ship

        if around_ship is not None:
            self.around_ship = around_ship
        else:
            self.around_ship = self.area_around_ship(ship)

        self.destroyed = False

    def __str__(self):
        cur = Cursor()
        cur._battlefield.place_ship(self.ship)

        return '    a b c d e f g h i j\n\n' + \
               cur._battlefield._field_values_to_show
