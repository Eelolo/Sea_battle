from battlefield.functions import new_field


FIELD_KEYS = list(new_field().keys())

FIELD_POINTS = list(set(FIELD_KEYS) - {str(num) for num in range(1,11)})

ERRORS = {
    'check_point_value': 'Start point must be like "1a" or "6d", in range 1a-10j.',
    'check_length': 'Length must be equal to {}.',
    'is_straight_check': 'Ship points must be lined up.',
    'points_on_field_check': 'Entered point not from a field.',
    'check_for_matches': 'Ship is too close to another.'
}

METHODS = ['up', 'down', 'left', 'right']

REVERSED = {
            'right': 'left',
            'left': 'right',
            'down': 'up',
            'up': 'down'
        }

PERPENDICULAR = {
            'right': ('up', 'down'),
            'left': ('up', 'down'),
            'down': ('right', 'left'),
            'up': ('right', 'left')
        }

SHIPS_EMPTY_SET = {
        4: {
            0: []
        },
        3: {
            0: [],
            1: []
        },
        2: {
            0: [],
            1: [],
            2: []
        },
        1: {
            0: [],
            1: [],
            2: [],
            3: []
        }
    }

SHIPS_ATTR_NAMES = {
    4:'fourdeck',
    3:'tripledeck',
    2:'doubledeck',
    1:'singledeck'
}

SEARCH_PLAN = [
    '7a', '8b', '9c', '10d',
    '3a', '4b', '5c', '6d', '7e', '8f', '9g', '10h',
    '1c', '2d', '3e', '4f', '5g', '6h', '7i', '8j',
    '1g', '2h', '3i', '4j',
    '10g', '9h', '8i', '7j',
    '10c', '9d', '8e', '7f', '6g', '5h', '4i', '3j',
    '8a', '7b', '6c', '5d', '4e', '3f', '2g', '1h',
    '4a', '3b', '2c', '1d'
]