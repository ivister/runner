import paramiko
import argparse
import os
from commandformer import DockerCommand
from arguments import LoadArguments


def get_filename():
    parser = argparse.ArgumentParser(description="Get file")
    parser.add_argument('-f', '--file', dest='filename', action='store', required=True)
    return parser.parse_args().filename


def load_image(client, image_name):
    args = LoadArguments(image_name)
    load_command = DockerCommand(command_type=DockerCommand.Load, arguments=args)

    stdin, stdout, stderr = client.exec_command(load_command.__str__())
    data = stdout.read() + stderr.read()
    print(data.decode())
    stdin.flush()
    stdout.flush()
    stderr.flush()


def configure_machine(hostname, image_name):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname)

    load_image(client=client, image_name=image_name)

    client.close()

if __name__ == '__main__':
    image_name = "/home/Alex/New/" + "image.tar"
    configure_machine('manager', image_name)
