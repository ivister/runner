"""
"""
import json
import argparse
import paramiko
from network import EthernetNetwork
from container import Container
from default import DEFAULT_VOLUMES, DEFAULT_ADAPTER
from swarm import Swarm


def get_filename():
    """
    :return:
    """
    parser = argparse.ArgumentParser(description="Get file")
    parser.add_argument('-f', '--file', dest='filename',
                        action='store', required=True)
    return parser.parse_args().filename


def parse_task_file(filename):
    """
    :param filename:
    :return:
    """
    with open(filename) as json_file:
        data = json.load(json_file)
    user = data["user"]
    image_file = data["image_file"]
    task_id = data["task_id"]
    machines = data["machines"].split(" ")

    return user, image_file, task_id, machines


def export_task_info(task_id, machines):
    """
    :param task_id:
    :param machines:
    :return:
    """
    with open("task.txt", "w") as json_file:
        json.dump(
            {
                "container": task_id,
                "machines": " ".join(machines)
            },
            json_file
        )


def multiply_image(image_file, machines):
    """
    :param image_file:
    :param machines:
    :return:
    """
    for mach in machines:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(mach)

        ftp = ssh.open_sftp()
        ftp.put(image_file, image_file)
        ftp.close()


def get_image_name(data):
    """
    :param data:
    :return:
    """
    """Input example b'Image Loaded: newmpich:latest' """
    tmp = data.decode().split(" ")
    return tmp[-1][:-1]


def get_load_command(image_file):
    return "docker load -i %s" % image_file


def load_image(client, image_file):
    """
    :param client:
    :param image_file:
    :return:
    """
    load_command = get_load_command(image_file)
    stdin, stdout, stderr = client.exec_command(load_command)
    data = stdout.read()
    _ = stderr.read()

# TODO:log errors
    image_name = get_image_name(data)

    stdin.flush()
    stdout.flush()
    stderr.flush()
# TODO: DEBUG
    rm_command = "rm -rf " + image_file
    _, _, stderr = client.exec_command(rm_command)
    _ = stderr.read()
    return image_name


def create_network(client, eth_net):
    """
    :param client:
    :param eth_net:
    :return:
    """
    stdin, stdout, stderr = client.exec_command(eth_net.create_command)
    data = stdout.read()
    _ = stderr.read()

    # TODO:log errors
    net_id = data.decode()

    stdin.flush()
    stdout.flush()
    stderr.flush()
    return net_id


def run_image(client, image_name, task_id, user):
    """
    :param client:
    :param image_name:
    :param task_id:
    :param user:
    :return:
    """
    container = Container(volumes=DEFAULT_VOLUMES,
                          detach=True,
                          name=task_id,
                          user=user,
                          image=image_name)
    run_command = container.run_command

    # TODO: DEBUG

    print(run_command)

    stdin, stdout, stderr = client.exec_command(run_command)
    stdin.flush()
    stdout.flush()
    stderr.flush()


def configure_machine(hostname, image_file, task_id, user, swarm_token=None):
    """
    :param hostname:
    :param image_file:
    :param task_id:
    :param user:
    :return:
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname)

    if no swarm_token:
        Swarm.init_swarm(client)
    else:
        Swarm.connect_to_swarm(client, swarm_token)

    network = EthernetNetwork(attachable=True, name=task_id,
                              driver="overlay", subnet="192.168.1.0/24")

    create_network(client, network)
    image_name = load_image(client=client, image_file=image_file)

    run_image(client=client, image_name=image_name, task_id=task_id, user=user)
    client.close()

    return network.get_name()


def main():
    filename = get_filename()
    user, image, task_id, machines = parse_task_file(filename)
    multiply_image(image, machines)

    for mach in machines:
        configure_machine(hostname=mach, image_file=image,
                          task_id=task_id, user=user)

    export_task_info(task_id=task_id, machines=machines)

if __name__ == '__main__':
    main()
