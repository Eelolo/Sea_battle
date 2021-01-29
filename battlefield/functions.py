def new_field():
    new_field = {}
    integers = [str(integer) for integer in range(1, 11)]
    letters = [chr(letter) for letter in (range(ord('a'), ord('k')))]
    field_keys = []

    for num in range(10):
        field_keys.append(str(num + 1))
        for idx in range(len(letters)):
            field_keys.append(integers[num] + letters[idx])

    for key in field_keys:
        if 'j' in key:
            new_field[key] = ' ~\n'
        elif len(key) == 1:
            new_field[key] = key + '  '
        elif key == '10':
            new_field[key] = '10 '
        else:
            new_field[key] = ' ~'

    return new_field


def check_point_value(point):
    message = 'Start point must be like "1a" or "6d", in range 1a-10j.'

    try:
        integer = int(point[:-1])
        letter = ord(point[-1])
    except ValueError:
        raise ValueError(message)

    if integer not in range(1, 11) or letter not in range(97, 107):
        raise ValueError(message)