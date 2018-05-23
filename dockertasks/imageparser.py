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

    def __write__(self, section, param, value):

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
        return self.__read__("General", "task_name").strip()

    @property
    def user(self):
        return self.__read__("General", "user").strip()

    @property
    def group(self):
        return self.__read__("General", "group").strip()


a = ImageParser()
print(a.nodes)
print(a.group)
print(a.task_name)
print(a.user)
