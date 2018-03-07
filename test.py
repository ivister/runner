import paramiko
import argparse
import json
from scp import SCPClient
from commandformer import DockerCommand
from arguments import LoadArguments, RunArguments


def get_filename():
    parser = argparse.ArgumentParser(description="Get file")
    parser.add_argument('-f', '--file', dest='filename', action='store', required=True)
    return parser.parse_args("-f test_file.txt".split()).filename


def parse_task_file(filename="test_file.txt"):
    with open(filename) as json_file:
        data = json.load(json_file)
    user = data["user"]
    image_file = data["image_file"]
    task_id = data["task_id"]
    machines = data["machines"].split(" ")

    return user, image_file, task_id, machines


def form_commands(user, image_file):
    load_command = DockerCommand(command_type=DockerCommand.Load,
                                 arguments=LoadArguments(image_file)).__str__()


# TODO: get image_name from image_file
    image_name = "newmpich"

    run_command = DockerCommand(command_type=DockerCommand.Run,
                                arguments=RunArguments(
                                    volumes="/home:/home",
                                    name=task_id,
                                    user=user,
                                    image_name=image_name
                                )).__str__()


def multiply_image(image_file, machines):
    for mach in machines:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(mach)

        with SCPClient(ssh.get_transport()) as scp:
            scp.put(image_file)


def get_image_name(data):
    """
    :param data:
    :return:
    """
    """Input example b'Image Loaded: newmpich:latest' """
    tmp = data.decode().split(" ")
    return tmp[-1]


def load_image(client, image_file):
    args = LoadArguments(image_file)
    load_command = DockerCommand(command_type=DockerCommand.Load, arguments=args)
    stdin, stdout, stderr = client.exec_command(load_command.__str__())
    data = stdout.read()
    errors = stderr.read()

# TODO:log errors
    image_name = get_image_name(data)

    stdin.flush()
    stdout.flush()
    stderr.flush()
    return image_name


def run_image(client, image_name, ):
    args = LoadArguments(image_name)
    load_command = DockerCommand(command_type=DockerCommand.Load, arguments=args)

    stdin, stdout, stderr = client.exec_command(load_command.__str__())
    data = stdout.read() + stderr.read()
    print(data.decode())
    stdin.flush()
    stdout.flush()
    stderr.flush()


def configure_machine(hostname, image_file):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname)

    image_name = load_image(client=client, image_file=image_file)
    run_image(client=client, image_name=image_name)

    client.close()

if __name__ == '__main__':
    filename = get_filename()
    user, image, task_id, mach = parse_task_file(filename)
    print(image)
    multiply_image(image, mach)
