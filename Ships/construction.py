from random import choice, randint


def new_ship(length, **kwargs):
    try:
        if kwargs['orientation'] != 'hor' or 'vert':
            raise ValueError('Orientation must be "hor" or "vert"')
        orientation = kwargs['orientation']
    except KeyError:
        orientation = choice(('hor', 'vert'))

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
