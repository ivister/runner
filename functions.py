def get_remote_name(task_id):
    prefix = ""
    return prefix + task_id + ".tar"


def dict_to_string(in_dict):

    result = ""
    for key in in_dict.keys():
        result += ' --%s=%s' % (key, in_dict[key])
    return result


def volumes_to_string(vol_string):
    tmp = vol_string.split(" ")
    result = ""
    for vol in tmp:
        result += " --volume %s" % vol
    return result
