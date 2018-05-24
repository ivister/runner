"""
"""
import json
import sys
import argparse
from subprocess import run, PIPE
import paramiko
from dockertasks.network import EthernetNetwork
from dockertasks.container import Container
from dockertasks.default import DEFAULT_VOLUMES
from dockertasks.default import DEFAULT_CPU_PER_NODE
# from swarm import Swarm
from dockertasks.functions import get_remote_name
from dockertasks.functions import dot_to_underscore
from dockertasks.functions import add_dot_txt
from dockertasks.functions import calculate_cpus
from dockertasks.functions import get_username_from_pair
from dockertasks.functions import move_hostfile_to_userhome
from dockertasks.executor import run_user_command
from dockertasks.imageparser import ImageParser


DEBUG_MODE = False


def get_hostname_filename():
    """
    :return:
    """
    parser = argparse.ArgumentParser(description="Get file")
    parser.add_argument('-f', '--file', dest='filename',
                        action='store', required=True)
    parser.add_argument('-n', '--node', dest='hostname',
                        action='store', required=False)
    return parser.parse_args().filename, parser.parse_args().hostname


def get_hostname():
    """
    :return:
    """
    parser = argparse.ArgumentParser(description="Get hostname")
    parser.add_argument('-n', '--node', dest='hostname',
                        action='store', required=True)
    return parser.parse_args().hostname


# def parse_task_file(filename):
#     """
#     :param filename:
#     :return:
#     """
#     with open(filename) as json_file:
#         data = json.load(json_file)
#     user = data["user"]
#     image_file = data["image_file"]
#     task_id = data["task_id"]
#     cpu_count = int(data["cpu"])
#     machines = data["hosts"].split(" ")
#     command = data["command"]
#
#     return user, image_file, task_id, machines, cpu_count, command
#
#
# def export_task_info(task_id, machines):
#     """
#     :param task_id:
#     :param machines:
#     :return:
#     """
#     with open(add_dot_txt(task_id), "w") as json_file:
#         json.dump(
#             {
#                 "task_id": task_id,
#                 "machines": " ".join(machines)
#             },
#             json_file
#         )
# def multiply_image(image_file, machines, task_id):
#     """
#     :param image_file:
#     :param machines:
#     :return:
#     """
#     for mach in machines:
#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         ssh.connect(mach)
#
#         ftp = ssh.open_sftp()
#         ftp.put(image_file, get_remote_name(task_id))
#         ftp.close()
#         ssh.close()


def get_image_name(data):
    """
    :param data:
    :return:
    """
    """Input example b'Image Loaded: newmpich:latest' """
    tmp = data.decode().split(" ")
    return tmp[-1][:-1]


def get_load_command(image_file):
    return ["docker", "load", "-i", image_file]


def load_image():
    """
    :param client:
    :param image_file:
    :return:
    """
    hostname = get_hostname()
    imagefile = get_hostname_filename()

    task_image = ImageParser(imagefile)
    load_command = get_load_command(task_image.docker_image_file)

    read = run(load_command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    return_code = read.returncode

    if not return_code == 0:
        sys.exit(return_code)
    image_name = get_image_name(read.stdout)

    if hostname == task_image.first_host:
        task_image.write("Docker", "docker_image", image_name)

    return 0


def create_network():
    """
    :return:
    """
    filename = get_hostname_filename()
    task_image = ImageParser(filename)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=task_image.first_host)

    network = EthernetNetwork(attachable=True, name=task_image.task_name,
                              driver="calico", ipam_driver="calico")
    stdin, stdout, stderr = client.exec_command(network.create_command)

    _ = stdout.read()
    _ = stderr.read()

    # TODO:log errors

    stdin.flush()
    stdout.flush()
    stderr.flush()
    client.close()
    return 0


def create_hostsfile():
    filename = get_hostname_filename()
    task_image = ImageParser(filename)
    hf_name = move_hostfile_to_userhome(nodes=task_image.nodes,
                                        task_id=task_image.task_name,
                                        user=task_image.user)
    task_image.write("Docker", "hostfile", hf_name)
    return 0


def run_image():

    filename, hostname = get_hostname_filename()
    task_image = ImageParser(filename)
    container = Container(volumes=DEFAULT_VOLUMES,
                          detach=True,
                          name="%s-%s" % (hostname, task_image.task_name),
                          net=task_image.task_name,
                          user=task_image.user,
                          cpus=task_image.nodes[hostname],
                          image=task_image.docker_image)
    run_command = container.run_command

    # TODO: DEBUG

    print(run_command)

    # stdin, stdout, stderr = client.exec_command(run_command)
    # stdout.read()
    # stderr.read()
    # stdin.flush()
    # stdout.flush()
    # stderr.flush()


def configure_machine(hostname, task_id, user, cpu_count, network_need=False):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname)

    # if not swarm_token:
    #     swarm_token = Swarm.init_swarm(client)
    # else:
    #     Swarm.connect_to_swarm(client, swarm_token)
    if network_need:
        network = EthernetNetwork(attachable=True, name=task_id,
                                  driver="calico", ipam_driver="calico")
        create_network(client, network)

    image_name = load_image(client=client, image_file=get_remote_name(task_id))

    run_image(client=client, image_name=image_name, task_id=task_id, user=user,
              main_hostname=hostname, cpu_count=cpu_count)
    client.close()

    # return swarm_token


def main():
    filename = get_filename()
    #user, image, or_task_id, machines, cpu_count, user_command = parse_task_file(filename)
    #task_id = dot_to_underscore(or_task_id)
    #multiply_image(image, machines, task_id)

    #cpu_per_node, cpu_last_node = calculate_cpus(machines, cpu_count, cpu_per_node=DEFAULT_CPU_PER_NODE)
    # swarm_token = None
    #for num, mach in enumerate(machines):
    #     if num == 0:
    #         cpu = cpu_last_node
    #         network = True
    #     else:
    #         network = False
    #         cpu = cpu_per_node
    #     configure_machine(hostname=mach, task_id=task_id,
    #                       user=user, cpu_count=cpu, network_need=network)
    #
    # #export_task_info(task_id=or_task_id, machines=machines)
    #
    # move_hostfile_to_userhome(nodes=machines, task_id=task_id,
    #                           user=get_username_from_pair(user), filename="hst")
    # # user_command = add_hostfile_to_command(user_command, hostfile_name=add_dot_txt(task_id))
    # run_user_command(task_id=task_id, host=machines[0], command=user_command)


if __name__ == '__main__':
    run_image()
