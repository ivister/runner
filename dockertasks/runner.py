"""
"""
import socket
import argparse
import paramiko
from dockertasks.network import EthernetNetwork
from dockertasks.container import Container
from dockertasks.default import DEFAULT_VOLUMES
from dockertasks.patterns import CONT_NAME_PAT, USER_DOCK_PAT
from dockertasks.functions import make_hostsfile
from dockertasks.imageparser import ImageParser
from dockertasks.functions import exec_local, generate_hosts_list


DEBUG_MODE = True


def get_filename():
    """
    :return:
    """
    parser = argparse.ArgumentParser(description="Get file")
    parser.add_argument('-f', '--file', dest='filename',
                        action='store', required=True)
    return parser.parse_args().filename


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

    imagefile = get_filename()
    hostname = socket.gethostname()

    task_image = ImageParser(imagefile)
    load_command = get_load_command(task_image.docker_image_file)

    _, out, err = exec_local(load_command)
    image_name = get_image_name(out)

    if hostname == task_image.first_host:
        task_image.write("Docker", "docker_image", image_name)

    return 0


def create_network():
    """
    :return:
    """
    filename = get_filename()
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
    filename = get_filename()
    task_image = ImageParser(filename)
    real_hosts, virt_hosts = generate_hosts_list(nodes=task_image.nodes, task_id=task_image.task_name)
    for index, hst in enumerate(real_hosts):
        task_image.write(section="Containers", param=hst, value=virt_hosts[index])
    hf_name = make_hostsfile(hosts_list=virt_hosts,
                             task_id=task_image.task_name,
                             user=task_image.user)
    task_image.write("Docker", "hostsfile", hf_name)
    return 0


def run_image():

    filename = get_filename()
    hostname = socket.gethostname()
    task_image = ImageParser(filename)

    container = Container(volumes=DEFAULT_VOLUMES,
                          detach=True,
                          name=CONT_NAME_PAT % (hostname, task_image.task_name),
                          net=task_image.task_name,
                          user=USER_DOCK_PAT % (task_image.user, task_image.group),
                          cpus=task_image.nodes[hostname],
                          image=task_image.docker_image)
    run_command = container.run_command

    if DEBUG_MODE:
        print(run_command)

    rc, _, _ = exec_local(run_command)
    return rc


def main():
    pass
    #filename = get_filename()
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
    create_hostsfile()
    #run_image()
