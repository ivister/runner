import os
import sys
from subprocess import run, PIPE


class ImageParser(object):
    """
    """

    def __init__(self, image_file):
        if not os.path.exists(image_file):
            raise AttributeError("Incorrect image file. Image file  not exists.")
        self.config_name = image_file

    def __read__(self, section, param=None):
        read_command = ["confread", self.config_name, section]
        if param:
            read_command.append(param)
        read = run(read_command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        return_code = read.returncode
        if not return_code == 0:
            sys.exit(return_code)
        return read.stdout

    def write(self, section, param, value):

        write_command = ["confwrite", self.config_name, section, param, value]
        read = run(write_command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

        return_code = read.returncode
        if not read.returncode == 0:
            sys.exit(return_code)

    def get_cont_by_hostname(self, host):
        out_list = self.__read__('Containers').strip().split("\n")
        cont_dict = {pair.split("=")[0].strip(): pair.split("=")[1].strip()
                     for pair in out_list}
        return cont_dict[host]

    @property
    def nodes(self):
        out_list = self.__read__('Nodes').strip().split('\n')
        node_dict = {pair.split("=")[0].strip(): pair.split("=")[1].strip()
                     for pair in out_list}
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
    def docker_hostsfile(self):
        return self.__read__("Docker", "hostsfile").strip()

    @property
    def first_host(self):
        first_pair = self.__read__('Nodes').split()[0]
        return first_pair.split('=')[0]

    @property
    def interactive(self):
        if self.__read__("Redirections", "interactive").strip() == "yes":
            return True
        else:
            return False


if __name__ == '__main__':
    a = ImageParser("../started.img")
    print(a.nodes)
    # print(a.group)
    # print(a.task_name)
    # print(a.user)
    # print(a.docker_image)
    # print(a.docker_image_file)
    print(a.interactive)
    print(a.get_cont_by_hostname("node2"))

    # read = run(["find \\\n / \\\n | \\\n grep confread"], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    # print(read.stdout)
    # return_code = read.returncode


