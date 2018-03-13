

def dict_to_string(in_dict):

    result = ""
    for key in in_dict.keys():
        result += ' %s="%s"' % (key, in_dict[key])
    return result
