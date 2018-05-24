"""
"""
import paramiko
import argparse
from dockertasks.container import Container
from dockertasks.imageparser import ImageParser

def get_filename():
    """
    :return:
    """
    parser = argparse.ArgumentParser(description="Get file")
    parser.add_argument('-f', '--file', dest='filename',
                        action='store', required=True)
    return parser.parse_args().filename


def run_user_command():
    """"""
    task_image = ImageParser(get_filename())

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(task_image.first_host)
    cont_name = task_image.get_cont_by_hostname(task_image.first_host)
    _, _, _ = ssh_client.exec_command(
        Container.exec_command(container_name=cont_name,
                               command=task_image.docker_command))
    ssh_client.close()
