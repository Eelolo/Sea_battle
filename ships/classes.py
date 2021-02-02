from battlefield.classes import Cursor
from other.validation import Validation
from other.env_vars import load_variable


FIELD_KEYS = load_variable('FIELD_KEYS')
REVERSED = load_variable('REVERSED')
PERPENDICULAR = load_variable('PERPENDICULAR')


class Ship:
    validation = Validation()

    def __define_orientation(self):
        if self.__points_difference in (1, -1):
            orientation = 'hor'
        else:
            orientation = 'vert'

        return orientation

    def area_around_ship(self, points: list):
        self.validation.is_straight_check(points)

        if self.__points_difference in (1, -1):
            if self.__points_difference > 0:
                cur_method = 'right'
            else:
                cur_method = 'left'
        else:
            if self.__points_difference > 0:
                cur_method = 'down'
            else:
                cur_method = 'up'

        around_ship = []
        break_on = None
        for loop_idx in range(3):
            self.__cursor.move(points[0])

            if loop_idx == 0:
                around_ship.append(getattr(self.__cursor, REVERSED[cur_method])())
            else:
                getattr(self.__cursor, REVERSED[cur_method])()
                around_ship.append(getattr(self.__cursor, PERPENDICULAR[cur_method][loop_idx - 1])())

            if self.__cursor.point == points[0]:
                break_on = self._length - 1

            for move_idx in range(self._length + 1):
                around_ship.append(getattr(self.__cursor, cur_method)())
                if break_on is not None and move_idx == break_on:
                    break

        around_ship = list(set(around_ship) - set(points))

        return around_ship

    def __init__(self, points: list, around_ship=None):
        self.validation.points_on_field_check(points)
        self.validation.is_straight_check(points)

        self._length = len(points)
        self.__points_difference = self.validation.points_difference(points)
        self.__orientation = self.__define_orientation()
        self._points = points
        self.__cursor = Cursor()

        if around_ship is not None:
            self.validation.points_on_field_check(points)
            self.around_ship = around_ship
        else:
            self.around_ship = self.area_around_ship(points)

        self.destroyed = False

    def __setattr__(self, key, value):
        if self.__dict__.get('_points') is not None:
            if key == '_length' and value != len(self._points):
                    raise ValueError("Wrong length.")

            if key == '_points':
                raise ValueError('Сreate a new ship if required.')

        self.__dict__[key] = value

    def __str__(self):
        self.__cursor._field.place_ship(self._points)

        return self.__cursor._field
