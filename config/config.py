REVERSED_MOVES = {
            'right': 'left',
            'left': 'right',
            'down': 'up',
            'up': 'down'
        }

PERPENDICULAR_MOVES = {
            'right': ('up', 'down'),
            'left': ('up', 'down'),
            'down': ('right', 'left'),
            'up': ('right', 'left')
        }

SHIPS_EMPTY_SET = {
        4: {
            0: [[], []]
        },
        3: {
            0: [[], []],
            1: [[], []]
        },
        2: {
            0: [[], []],
            1: [[], []],
            2: [[], []]
        },
        1: {
            0: [[], []],
            1: [[], []],
            2: [[], []],
            3: [[], []]
        }
    }