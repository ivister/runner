"""
"""
import json
import os
import argparse
import paramiko
from dockertasks.container import Container
from dockertasks.network import EthernetNetwork
from dockertasks.imageparser import ImageParser
# from swarm import Swarm
from dockertasks.functions import dot_to_underscore


def get_filename():
    """
    :return:
    """
    parser = argparse.ArgumentParser(description="Get file")
    parser.add_argument('-f', '--file', dest='filename',
                        action='store', required=True)
    return parser.parse_args().filename


def remove_hostsfile():
    filename = get_filename()
    task_image = ImageParser(filename)
    os.remove(task_image.docker_hostsfile)


def remove_docker_image():
    filename = get_filename()
    task_image = ImageParser(filename)
    rmi_cmd = Container.remove_image(task_image.docker_image)



def parse_stop_file(filename):
    """
    :param filename:
    :return:
    """
    with open(filename) as json_file:
        data = json.load(json_file)
    task_id = data["task_id"]
    machines = data["machines"].split(" ")
    return task_id, machines


def clean_machine(hostname, or_task_id):
    """
    :param hostname:
    :param cont_name:
    :return:
    """

    task_id = dot_to_underscore(or_task_id)
    cont_name = "%s-%s" % (hostname, task_id)

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname)

    _, stdout, stderr = ssh_client.exec_command(Container.img_from_cont(cont_name))
    image_name = stdout.read().decode()
    stdout.flush()

    _, stdout, stderr = ssh_client.exec_command(Container.stop(cont_name))
    _ = stdout.read().decode()
    stdout.flush()

    _, stdout, stderr = ssh_client.exec_command(Container.remove(cont_name))
    _ = stdout.read().decode()

    _, _, stderr = ssh_client.exec_command(Container.remove_image(image_name))

    _, _, stderr = ssh_client.exec_command(EthernetNetwork.remove(task_id))

    # _, _, stderr = ssh_client.exec_command(Swarm.get_leave_command())

    _ = stderr.read().decode()

    ssh_client.close()


def main():
    fn = get_filename()
    task_id, machines = parse_stop_file(fn)
    for mach in machines:
        clean_machine(mach, task_id)

    os.remove(fn)


if __name__ == '__main__':
    main()
