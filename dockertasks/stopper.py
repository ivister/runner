"""
"""
import json
import os
import argparse
import socket
import paramiko
from dockertasks.container import Container
from dockertasks.network import EthernetNetwork
from dockertasks.imageparser import ImageParser
from dockertasks.functions import dot_to_underscore
from dockertasks.functions import exec_local


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
    print(rmi_cmd)
    rc, _, _ = exec_local(rmi_cmd)
    return rc


def stop_cont():
    filename = get_filename()
    hostname = socket.gethostname()
    task_image = ImageParser(filename)
    stop_cmd = Container.stop_command(
        task_image.get_cont_by_hostname(host=hostname))
    print(stop_cmd)
    rc, _, _ = exec_local(stop_cmd)
    return rc


def remove_cont():
    filename = get_filename()
    hostname = socket.gethostname()
    task_image = ImageParser(filename)
    remove_cmd = Container.remove_command(
        task_image.get_cont_by_hostname(hostname))
    print(remove_cmd)
    rc, _, _ = exec_local(remove_cmd)
    return rc


def remove_net():
    filename = get_filename()
    task_image = ImageParser(filename)
    remove_cmd = EthernetNetwork.remove(task_image.task_name)
    print(remove_cmd)
    _, _, _ = exec_local(remove_cmd)
    return 0


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


if __name__ == '__main__':
    remove_net()
    remove_docker_image()
    remove_cont()
    stop_cont()
