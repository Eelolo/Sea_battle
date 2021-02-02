from .env_vars import load_variable
from config.config import ERRORS


FIELD_KEYS = load_variable('FIELD_KEYS')
FIELD_POINTS = load_variable('FIELD_POINTS')
METHODS = load_variable('METHODS')


class Validation:
    def is_int(self, instance, inst_name):
        if not isinstance(instance, int):
            raise TypeError('{} must be a integer.'.format(inst_name))

        return isinstance(instance, int)

    def is_str(self, instance, inst_name):
        if not isinstance(instance, str):
            raise TypeError('{} must be a string.'.format(inst_name))

        return isinstance(instance, str)

    def is_list(self, instance, inst_name):
        if not isinstance(instance, list):
            raise TypeError('{} must be a list.'.format(inst_name))

        return isinstance(instance, list)

    def check_point_value(self, point: str):
        message = ERRORS['check_point_value']

        try:
            integer = int(point[:-1])
            letter = ord(point[-1])
        except TypeError:
            raise ValueError(message)

        if integer not in range(1, 11) or letter not in range(97, 107):
            raise ValueError(message)

    def points_difference(self, points: list):
        self.is_list(points, 'Points')

        for point in points:
            self.check_point_value(point)

        if len(points) == 1:
            points_difference = 1
        else:
            points_difference = FIELD_KEYS.index(points[1]) - FIELD_KEYS.index(points[0])

        return points_difference

    def check_length(self, points: list, length: int):
        self.is_list(points, 'Points')
        self.is_int(length, 'Length')

        if len(points) != length:
            print(ERRORS['check_length'].format(length))

            return False

        return True

    def check_for_matches(self, array0, array1, message=False):
        self.is_list(array0, 'Array0')
        self.is_list(array0, 'Array1')

        if set(array0) & set(array1) == set():
            return True
        else:
            if message:
                print(ERRORS['check_for_matches'])

            return False

    def points_on_field_check(self, points, message=False):
        if isinstance(points, list):
            points = set(points)

            if len(points) > 1:
                message = ERRORS['points_on_field_check'].replace('point', 'points')

        elif isinstance(points, str):
            points = {points}
        else:
            raise TypeError('Points must be list or string')

        if points - set(FIELD_POINTS) != set():
            if message:
                print(ERRORS['points_on_field_check'])
            else:
                raise ValueError(ERRORS['points_on_field_check'])

            return False

        return True

    def is_straight_check(self, points: list, message=False):
        self.is_list(points, 'Points')

        if len(points) == 1:
            return True
        elif '' in points:
            return False

        point_difference = self.points_difference(points)

        if point_difference in (1, -1):
            orientation = 'hor'
        else:
            orientation = 'vert'

        for idx in range(len(points) - 1):
            point_difference = FIELD_KEYS.index(points[idx + 1]) - FIELD_KEYS.index(points[idx])

            if orientation == 'hor' and point_difference not in (1, -1) or \
                    orientation == 'vert' and point_difference not in (11, -11):
                if message:
                    print(ERRORS['is_straight_check'])
                else:
                    raise ValueError(ERRORS['is_straight_check'])

                return False

        return True

    def check_method(self, method):
        if method not in METHODS:
            raise AttributeError("Move must be in: 'up', 'down', 'left', 'right'")
