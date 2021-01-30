from config.config import FIELD_KEYS, FIELD_POINTS, ERRORS, METHODS


class Validation:
    def points_difference(self, points):
        if len(points) == 1:
            points_difference = 1
        else:
            points_difference = FIELD_KEYS.index(points[1]) - FIELD_KEYS.index(points[0])

        return points_difference

    def check_point_value(self, point):
        message = ERRORS['check_point_value']

        try:
            integer = int(point[:-1])
            letter = ord(point[-1])
        except ValueError:
            raise ValueError(message)

        if integer not in range(1, 11) or letter not in range(97, 107):
            raise ValueError(message)

    def check_length(self, points, length):
        if len(points) != length:
            print(ERRORS['check_length'].format(length))

            return False

        return True

    def is_straight_check(self, points, message=False):
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

    def points_on_field_check(self, points, message=False):
        if isinstance(points, list):
            points = set(points)

            if len(points) > 1:
                message = ERRORS['points_on_field_check'].replace('point', 'points')

        elif isinstance(points, str):
            points = {points}
        else:
            raise TypeError('points must be list or string')

        if points - set(FIELD_POINTS) != set():
            if message:
                print(ERRORS['points_on_field_check'])
            else:
                raise ValueError(ERRORS['points_on_field_check'])

            return False

        return True

    def check_for_matches(self, array0, array1, message=False):
        if set(array0) & set(array1) == set():
            return True
        else:
            if message:
                print(ERRORS['check_for_matches'])

            return False
