"""
"""
from dockertasks.patterns import HOSTNAME_DOCK_PAT, HOSTSFILE_PAT
import shutil
import pwd
import os
import sys
from subprocess import run, PIPE


def dict_to_string(in_dict):
    result = ""
    for key in in_dict.keys():
        if "_" in key:
            result += ' --%s=%s \\\n' % ("-".join(key.split("_")), in_dict[key])
        else:
            result += ' --%s=%s \\\n' % (key, in_dict[key])
    return result


def dict_to_list(in_dict):
    result = []
    for key in in_dict.keys():
        if "_" in key:
            result.append('--%s=%s' % ("-".join(key.split("_")), in_dict[key]))
        else:
            result.append('--%s=%s' % (key, in_dict[key]))
    return result


def volumes_to_list(vol_string):
    tmp = ["--volume=%s" % vol for vol in vol_string.split(" ")]
    return tmp


def dot_to_underscore(dot_text):
    return "-".join(dot_text.split("."))


def add_dot_txt(filename):
    return filename + ".txt"


def add_hostfile_to_command(command, hostfile_name="hostfile.txt"):
    if ("--hostfile" in command) or ("-h" in command):
        return command
    else:
        tmp = command.split(" ")
        tmp[0] += " --hostfile %s " % hostfile_name
        return " ".join(tmp)


def generate_hosts_list(nodes, task_id):
    """
    :param nodes:
    :param task_id:
    :return:
    """
    keys = [key for key in nodes.keys()]
    hostnames = [HOSTNAME_DOCK_PAT % (task_id, key, task_id) for key in keys]
    return keys, hostnames


def write_hosts_to_file(hosts_list, filename):
    with open(filename, "w") as fil:
        fil.write("\n".join(hosts_list))
    return filename


def make_hostsfile(hosts_list, task_id, user):
    homedir = pwd.getpwnam(user)[5] + "/"
    filename = homedir + HOSTSFILE_PAT % (task_id, "hostfile")
    with open(filename, "w") as fil:
        fil.write("\n".join(hosts_list))

    os.chmod(filename, 0o666)
    shutil.copy(filename, homedir)
    os.remove(filename)

    return "%s/%s" % (homedir, filename)


def exec_local(cmd):
    thread = run(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    return_code = thread.returncode
    out = thread.stdout
    err = thread.stderr
    if not return_code == 0:
        sys.exit(return_code)
    return return_code, out, err


if __name__ == '__main__':
    pass
    # print(dot_to_underscore("mpi.ivan.docker.net.33"))
    # l = ['a', 'b']
    # print(l.index('a'))
    #
    # tmp = generate_hosts_line(["node1", "node2", "node3", "node4"], "mpi_ivan_133")
    # print(add_hostfile_to_command("mpirun -np 3 -ppn 1 -h hostfile.txt ./task -a a1 -b b1",
    #                               hostfile_name="hostfile.txt"))
    # write_hosts_to_file(tmp, "hostfile.txt")
    #
    # calculate_cpus(["node1", "node3"], cpu_need=3, cpu_per_node=2)
    #
    #move_hostfile_to_userhome(["node1", "node2", "node3", "node4"], "mpi_ivan_133", "ivan", "hostfile.txt")
    # import pwd
    # d = pwd.getpwnam("ivan")
    # print(d)
