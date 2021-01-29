from battlefield.classes import Cursor
from config.config import REVERSED, PERPENDICULAR


class Ship:
    def points_difference(self, points):
        cur = Cursor()
        if len(points) == 1:
            points_difference = 1
        else:
            points_difference = cur._field_keys.index(points[1]) - cur._field_keys.index(points[0])

        return points_difference

    def define_orientation(self):
        if self.points_difference in (1, -1):
            orientation = 'hor'
        else:
            orientation = 'vert'

        return orientation

    def area_around_ship(self, points):
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

        cur = Cursor()
        around_ship = []
        break_on = None
        for loop_idx in range(3):
            cur.move(points[0])

            if loop_idx == 0:
                around_ship.append(getattr(cur, REVERSED[cur_method])())
            else:
                getattr(cur, REVERSED[cur_method])()
                around_ship.append(getattr(cur, PERPENDICULAR[cur_method][loop_idx - 1])())

            if cur.point == points[0]:
                break_on = self.length - 1

            for move_idx in range(self.length + 1):
                around_ship.append(getattr(cur, cur_method)())
                if break_on is not None and move_idx == break_on:
                    break

        around_ship = list(set(around_ship) - set(points))

        return around_ship

    def __init__(self, points, around_ship=None):
        self.length = len(points)
        self.points_difference = self.points_difference(points)
        self.orientation = self.define_orientation()
        self.points = points

        if around_ship is not None:
            self.around_ship = around_ship
        else:
            self.around_ship = self.area_around_ship(points)

        self.destroyed = False

    def __str__(self):
        cur = Cursor()
        cur._field.place_ship(self.points)

        return cur._field
