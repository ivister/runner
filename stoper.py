import paramiko
import argparse
import json


def get_filename():
    """
    :return:
    """
    parser = argparse.ArgumentParser(description="Get file")
    parser.add_argument('-f', '--file', dest='filename', action='store', required=True)
    return parser.parse_args("-f task.txt".split()).filename


def parse_stop_file(filename="test_file.txt"):
    """
    :param filename:
    :return:
    """
    with open(filename) as json_file:
        data = json.load(json_file)
    cont_name = data["container"]
    machines = data["machines"].split(" ")
    return cont_name, machines


def img_from_cont(cont_name):
    """
    :param cont_name:
    :return:
    """
    return "docker ps --filter=name=%s --format='{{.Image}}'" % cont_name


def clear_machine(hostname, cont_name):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname)

    stdin, stdout, stderr = client.exec_command(img_from_cont(cont_name=cont_name))
    image_name = stdout.read()
    stdin.flush()
    stdout.flush()
    stderr.flush()

    stdin, stdout, stderr = client.exec_command("docker stop %s" % cont_name)
    cont_id = stdout.read().decode()
    stdin.flush()
    stdout.flush()
    stderr.flush()

    stdin, stdout, stderr = client.exec_command("docker rmi %s" % image_name)
    stdin.flush()
    stdout.flush()
    stderr.flush()

    stdin, stdout, stderr = client.exec_command("docker container prune" % image_name)
    stdin.flush()
    stdout.flush()
    stderr.flush()

    client.close()


if __name__ == '__main__':
    fn = get_filename()
    cnt, mach = parse_stop_file(fn)
    for m in mach:
        clear_machine(m, cnt)
    pass
