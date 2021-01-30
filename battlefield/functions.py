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
