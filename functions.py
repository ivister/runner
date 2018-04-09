"""
"""
from default import DEFAULT_CPU_PER_NODE


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


def dot_to_underscore(dot_text):
    return "_".join(dot_text.split("."))


def add_dot_txt(filename):
    return filename + ".txt"


def calculate_cpus(machines, cpu_need, cpu_per_node=DEFAULT_CPU_PER_NODE):
    set_node_cpu = cpu_per_node
    last_node_cpu = cpu_need - (len(machines) - 1) * cpu_per_node
    print(set_node_cpu)
    print(last_node_cpu)
    return set_node_cpu, last_node_cpu


if __name__ == '__main__':
    print(dot_to_underscore("mpi.ivan.docker.net.33"))
    l = ['a', 'b']
    print(l.index('a'))

    calculate_cpus(["node1", "node3"], cpu_need=3, cpu_per_node=2)
