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


def parse_stop_file(filename="task.txt"):
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

    _, stdout, stderr = client.exec_command(img_from_cont(cont_name=cont_name))
    image_name = stdout.read().decode()
    stdout.flush()

    _, stdout, stderr = client.exec_command("docker stop %s" % cont_name)
    cont_id = stdout.read().decode()
    stdout.flush()

    _, stdout, stderr = client.exec_command("docker rm %s" % cont_id)
    check = stdout.read().decode()

    _, _, stderr = client.exec_command("docker rmi %s" % image_name)

    errors = stderr.read().decode()
    print(errors)

    client.close()


if __name__ == '__main__':
    fn = get_filename()
    cnt, mach = parse_stop_file(fn)
    for m in mach:
        clear_machine(m, cnt)
    pass
