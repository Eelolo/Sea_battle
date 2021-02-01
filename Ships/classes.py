from battlefield.classes import Cursor
from other.validation import Validation
from other.env_vars import load_variable


FIELD_KEYS = load_variable('FIELD_KEYS')
REVERSED = load_variable('REVERSED')
PERPENDICULAR = load_variable('PERPENDICULAR')


class Ship:
    validation = Validation()

    def define_orientation(self):
        if self.points_difference in (1, -1):
            orientation = 'hor'
        else:
            orientation = 'vert'

        return orientation

    def area_around_ship(self, points: list):
        self.validation.is_straight_check(points)

        if self.points_difference in (1, -1):
            if self.points_difference > 0:
                cur_method = 'right'
            else:
                cur_method = 'left'
        else:
            if self.points_difference > 0:
                cur_method = 'down'
            else:
                cur_method = 'up'

        around_ship = []
        break_on = None
        for loop_idx in range(3):
            self.cursor.move(points[0])

            if loop_idx == 0:
                around_ship.append(getattr(self.cursor, REVERSED[cur_method])())
            else:
                getattr(self.cursor, REVERSED[cur_method])()
                around_ship.append(getattr(self.cursor, PERPENDICULAR[cur_method][loop_idx - 1])())

            if self.cursor.point == points[0]:
                break_on = self.length - 1

            for move_idx in range(self.length + 1):
                around_ship.append(getattr(self.cursor, cur_method)())
                if break_on is not None and move_idx == break_on:
                    break

        around_ship = list(set(around_ship) - set(points))

        return around_ship

    def __init__(self, points: list, around_ship=None):
        self.validation.points_on_field_check(points)
        self.validation.is_straight_check(points)

        self.length = len(points)
        self.points_difference = self.validation.points_difference(points)
        self.orientation = self.define_orientation()
        self.points = points
        self.cursor = Cursor()

        if around_ship is not None:
            self.validation.points_on_field_check(points)
            self.around_ship = around_ship
        else:
            self.around_ship = self.area_around_ship(points)

        self.destroyed = False

    def __str__(self):
        self.cursor._field.place_ship(self.points)

        return self.cursor._field
