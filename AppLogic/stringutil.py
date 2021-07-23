def replace_kk(no_kk, start_position, char_length):
    ep = start_position
    length = char_length
    counter = 0
    new_string = ""
    for kar in no_kk:
        if ep <= counter <= ep + length:
            new_string += "X"
        else:
            new_string += kar
        counter += 1

    return new_string
