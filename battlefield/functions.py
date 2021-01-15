def new_battlefield():
    new_battlefield = {}
    integers = [str(integer) for integer in range(1, 11)]
    letters = [chr(letter) for letter in (range(ord('a'), ord('k')))]
    battlefield_keys = []

    for num in range(10):
        battlefield_keys.append(str(num + 1))
        for idx in range(len(letters)):
            battlefield_keys.append(integers[num] + letters[idx])

    for key in battlefield_keys:
        if 'j' in key:
            new_battlefield[key] = ' ~\n'
        elif len(key) == 1:
            new_battlefield[key] = key + '  '
        elif key == '10':
            new_battlefield[key] = '10 '
        else:
            new_battlefield[key] = ' ~'

    return new_battlefield
