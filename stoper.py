"""
"""
import json
import argparse
import paramiko
from container import Container
from network import EthernetNetwork


def get_filename():
    """
    :return:
    """
    parser = argparse.ArgumentParser(description="Get file")
    parser.add_argument('-f', '--file', dest='filename',
                        action='store', required=True)
    return parser.parse_args().filename


def parse_stop_file(filename):
    """
    :param filename:
    :return:
    """
    with open(filename) as json_file:
        data = json.load(json_file)
    cont_name = data["container"]
    machines = data["machines"].split(" ")
    return cont_name, machines


def clean_machine(hostname, cont_name):
    """
    :param hostname:
    :param cont_name:
    :return:
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname)

    _, stdout, stderr = client.exec_command(Container.img_from_cont(cont_name))
    image_name = stdout.read().decode()
    stdout.flush()

    _, stdout, stderr = client.exec_command(Container.stop(cont_name))
    _ = stdout.read().decode()
    stdout.flush()

    _, stdout, stderr = client.exec_command(Container.remove(cont_name))
    _ = stdout.read().decode()

    _, _, stderr = client.exec_command(Container.remove_image(image_name))

    print(stderr.read())
    _, _, stderr = client.exec_command(EthernetNetwork.remove(cont_name))

    errors = stderr.read().decode()
    print(errors)

    client.close()


def main():
    fn = get_filename()
    cnt, mach = parse_stop_file(fn)
    for m in mach:
        clean_machine(m, cnt)

if __name__ == '__main__':
    main()
