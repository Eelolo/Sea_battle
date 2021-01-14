from random import choice, randint


def new_ship(length, **kwargs):
    try:
        if kwargs['orientation'] not in ('hor', 'vert'):
            raise ValueError('Orientation must be "hor" or "vert".')
        orientation = kwargs['orientation']
    except KeyError:
        orientation = choice(('hor', 'vert'))

    try:
        if kwargs['start_point'][0] not in range(1,11) and ord(kwargs['start_point'][1]) not in range(97, 106):
            raise ValueError('Start point must be like "1a" or "6d", in range 1a-10j.')
        integer = int(kwargs['start_point'][0])
        letter = ord(kwargs['start_point'][1])
    except KeyError:
        integer = randint(1, 10)
        letter = randint(97, 106)

    ship = []
    if orientation == 'hor':
        if letter > 106 - length:
            for _ in range(length):
                ship.append(str(integer) + chr(letter))
                letter -= 1
        else:
            for _ in range(length):
                ship.append(str(integer) + chr(letter))
                letter += 1
    elif orientation == 'vert':
        if integer > 10 - length:
            for _ in range(length):
                ship.append(str(integer) + chr(letter))
                integer -= 1
        else:
            for _ in range(length):
                ship.append(str(integer) + chr(letter))
                integer += 1

    return ship
