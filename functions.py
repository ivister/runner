"""
"""
from default import DEFAULT_CPU_PER_NODE
from os import system


def get_remote_name(task_id):
    prefix = ""
    return prefix + task_id + ".tar"


def dict_to_string(in_dict):
    result = ""
    for key in in_dict.keys():
        if "_" in key:
            result += ' --%s=%s' % ("-".join(key.split("_")), in_dict[key])
        else:
            result += ' --%s=%s' % (key, in_dict[key])
    return result


def volumes_to_string(vol_string):
    tmp = vol_string.split(" ")
    result = ""
    for vol in tmp:
        result += " --volume=%s" % vol
    return result


def dot_to_underscore(dot_text):
    return "_".join(dot_text.split("."))


def add_dot_txt(filename):
    return filename + ".txt"


def calculate_cpus(machines, cpu_need, cpu_per_node=DEFAULT_CPU_PER_NODE):
    set_node_cpu = cpu_per_node
    last_node_cpu = cpu_need - (len(machines) - 1) * cpu_per_node
    # print(set_node_cpu)
    # print(last_node_cpu)
    return set_node_cpu, last_node_cpu


def get_username_from_pair(pair):
    return pair.split(":")[0]


def add_hostfile_to_command(command, hostfile_name="hostfile.txt"):
    if ("--hostfile" in command) or ("-h" in command):
        return command
    else:
        tmp = command.split(" ")
        tmp[0] += " --hostfile %s " % hostfile_name
        return " ".join(tmp)


def generate_hosts_line(machines, task_id):
    tmp = []
    for mach in machines:
        tmp.append("%s.%s" % (mach, task_id))
    return "\n".join(tmp)


def write_hosts_to_file(hosts_line, filename):
    with open(filename, "w") as fil:
        fil.write(hosts_line)
    return filename


def move_hostfile_to_userhome(user, filename):
    cmd_pattern = """sudo chown %s %s && su %s -c "mv %s ~/ && cat %s" """
    system(cmd_pattern % (user, filename, user, filename, filename))


if __name__ == '__main__':
    print(dot_to_underscore("mpi.ivan.docker.net.33"))
    l = ['a', 'b']
    print(l.index('a'))

    tmp = generate_hosts_line(["node1", "node2", "node3", "node4"], "mpi_ivan_133")
    print(add_hostfile_to_command("mpirun -np 3 -ppn 1 -h hostfile.txt ./task -a a1 -b b1",
                                  hostfile_name="hostfile.txt"))
    write_hosts_to_file(tmp, "hostfile.txt")

    calculate_cpus(["node1", "node3"], cpu_need=3, cpu_per_node=2)

    move_hostfile_to_userhome("ivan", "hostfile.txt")
