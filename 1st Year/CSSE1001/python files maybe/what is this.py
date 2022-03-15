def get_char_position (char_to_find, string):
    '''Return index of first occurence of 'cahr_to_find' in 'string'.'''
    for index, current_char in enumerate(string):
        if current_char == char_to_find:
            return index
    return -1

def double_list(list):
    '''Double all values in 'list'.'''
    for index in range(len(list)):
        list[index] *= 2
    return list

class help(object):
    def __init__():
