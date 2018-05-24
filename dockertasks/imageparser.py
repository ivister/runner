import os
import sys
from subprocess import run, PIPE


class ImageParser(object):
    """
    """

    def __init__(self, image_file="../started.img"):
        if not os.path.exists(image_file):
            raise AttributeError("Incorrect image file. Image file  not exists.")
        self.config_name = image_file

    def __read__(self, section, param=None):
        read_command = ["./../confread", self.config_name, section]
        if param:
            read_command.append(param)
        read = run(read_command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        return_code = read.returncode
        if not return_code == 0:
            sys.exit(return_code)
        return read.stdout

    def write(self, section, param, value):

        write_command = ["./../confwrite", self.config_name, section, param, value]
        read = run(write_command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

        return_code = read.returncode
        if not read.returncode == 0:
            sys.exit(return_code)

    @property
    def nodes(self):
        out_list = self.__read__('Nodes').split()
        node_dict = {pair.split("=")[0]: pair.split("=")[1] for pair in out_list}
        return node_dict

    @property
    def task_name(self):
        return self.__read__("General", "job_id").strip()

    @property
    def user(self):
        return self.__read__("General", "user").strip()

    @property
    def group(self):
        return self.__read__("General", "group").strip()

    @property
    def docker_image_file(self):
        return self.__read__("Docker", "docker_image_file").strip()

    @property
    def docker_image(self):
        return self.__read__("Docker", "docker_image").strip()

    @property
    def docker_command(self):
        return self.__read__("Docker", "docker_command").strip()

    @property
    def first_host(self):
        first_pair = self.__read__('Nodes').split()[0]
        return first_pair.split('=')[0]


if __name__ == '__main__':
    a = ImageParser()
    print(a.nodes)
    print(a.group)
    print(a.task_name)
    print(a.user)
    print(a.docker_image)
    print(a.docker_image_file)
    print(a.docker_command)
    print(a.first_host)

