"""
"""
import json
import argparse
import paramiko
from network import EthernetNetwork
from container import Container
from default import DEFAULT_VOLUMES
from default import DEFAULT_CPU_PER_NODE
from swarm import Swarm
from functions import get_remote_name
from functions import dot_to_underscore
from functions import add_dot_txt
from functions import calculate_cpus


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
    cpu_count = int(data["cpu_count"])
    machines = data["machines"].split(" ")
    try:
        if data["enable_infiniband"] == "yes":
            enable_ib = True
        else:
            enable_ib = False
    except Exception:
        enable_ib = False

    return user, image_file, task_id, machines, cpu_count, enable_ib


def export_task_info(task_id, machines):
    """
    :param task_id:
    :param machines:
    :return:
    """
    with open(add_dot_txt(task_id), "w") as json_file:
        json.dump(
            {
                "task_id": task_id,
                "machines": " ".join(machines)
            },
            json_file
        )


def multiply_image(image_file, machines, task_id):
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
        ftp.put(image_file, get_remote_name(task_id))
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
    print(eth_net.create_command)
    data = stdout.read()
    _ = stderr.read()

    # TODO:log errors
    net_id = data.decode()

    stdin.flush()
    stdout.flush()
    stderr.flush()
    return net_id


def run_image(client, image_name, task_id, user, main_hostname, enable_ib, cpu_count=DEFAULT_CPU_PER_NODE):

    container = Container(volumes=DEFAULT_VOLUMES,
                          detach=True,
                          name=task_id,
                          net=task_id,
                          hostname="%s.%s" % (main_hostname, task_id),
                          user=user,
                          enable_ib=enable_ib,
                          cpus=cpu_count,
                          image=image_name)
    run_command = container.run_command

    # TODO: DEBUG

    print(run_command)

    stdin, stdout, stderr = client.exec_command(run_command)
    stdin.flush()
    stdout.flush()
    stderr.flush()


def configure_machine(hostname, task_id, user, swarm_token, cpu_count, enable_ib=False):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname)

    if not swarm_token:
        swarm_token = Swarm.init_swarm(client)
    else:
        Swarm.connect_to_swarm(client, swarm_token)

    network = EthernetNetwork(attachable=True, name=task_id,
                              driver="overlay", subnet="64.0.0.0/8")

    create_network(client, network)
    image_name = load_image(client=client, image_file=get_remote_name(task_id))

    run_image(client=client, image_name=image_name, task_id=task_id, user=user,
              main_hostname=hostname, cpu_count=cpu_count)
    client.close()

    return swarm_token


def main():
    filename = get_filename()
    user, image, or_task_id, machines, cpu_count, enable_ib = parse_task_file(filename)
    task_id = dot_to_underscore(or_task_id)
    multiply_image(image, machines, task_id)

    cpu_per_node, cpu_last_node = calculate_cpus(machines, cpu_count, cpu_per_node=DEFAULT_CPU_PER_NODE)

    swarm_token = None
    for mach in machines:
        print(swarm_token)
        if machines.index(mach) == 0:
            swarm_token = configure_machine(hostname=mach, task_id=task_id,
                                            user=user, swarm_token=swarm_token,
                                            cpu_count=cpu_last_node, enable_ib=enable_ib)
        else:
            swarm_token = configure_machine(hostname=mach, task_id=task_id,
                                            user=user, swarm_token=swarm_token,
                                            cpu_count=cpu_per_node, enable_ib=enable_ib)

    export_task_info(task_id=or_task_id, machines=machines)


if __name__ == '__main__':
    main()
