import paramiko
import argparse
import json
from scp import SCPClient
from commandformer import DockerCommand
from arguments import LoadArguments, RunArguments


def get_filename():
    parser = argparse.ArgumentParser(description="Get file")
    parser.add_argument('-f', '--file', dest='filename', action='store', required=True)
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
    with open("task.txt", "w") as json_file:
        json.dump(
            {
                "container": task_id,
                "machines": " ".join(machines)
            },
            json_file
        )


def multiply_image(image_file, machines):
    for mach in machines:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(mach)

        ftp = ssh.open_sftp()
        ftp.put(image_file, image_file)
        ftp.close()
        # with SCPClient(ssh.get_transport()) as scp:
        #    scp.put(image_file)


def get_image_name(data):
    """
    :param data:
    :return:
    """
    """Input example b'Image Loaded: newmpich:latest' """
    tmp = data.decode().split(" ")
    return tmp[-1][:-1]


def load_image(client, image_file):
    args = LoadArguments(image_file)
    load_command = DockerCommand(command_type=DockerCommand.Load,
                                 arguments=args).__str__()
    stdin, stdout, stderr = client.exec_command(load_command)
    data = stdout.read()
    errors = stderr.read()

# TODO:log errors
    image_name = get_image_name(data)

    stdin.flush()
    stdout.flush()
    stderr.flush()

    rm_command = "rm -rf " + image_file
    _, _, stderr = client.exec_command(rm_command)
    return image_name


def run_image(client, image_name, task_id):
    args = RunArguments(
                                    volumes="/home:/home",
                                    name=task_id,
                                    user=user,
                                    image_name=image_name
                                )
    run_command = DockerCommand(command_type=DockerCommand.Run,
                                arguments=args).__str__()

    stdin, stdout, stderr = client.exec_command(run_command)
    stdin.flush()
    stdout.flush()
    stderr.flush()


def configure_machine(hostname, image_file):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname)

    load_command = DockerCommand(command_type=DockerCommand.Load,
                                 arguments=LoadArguments(image_file)).__str__()

    image_name = load_image(client=client, image_file=image_file)

    run_image(client=client, image_name=image_name, task_id=task_id)
    client.close()

    return image_name

if __name__ == '__main__':
    filename = get_filename()
    user, image, task_id, machines = parse_task_file(filename)
    multiply_image(image, machines)
    image_name = ""
    for mach in machines:
        image_name = configure_machine(hostname=mach, image_file=image)

    export_task_info(task_id=task_id, machines=machines)
