"""
"""

from dockertasks.functions import volumes_to_list
from dockertasks.functions import dict_to_list


class Container(object):
    """
    """
    __available_args = ["volumes",
                        "devices",
                        "hostname",
                        "net",
                        "user",
                        "image",
                        "detach",
                        "interactive",
                        "cpus",
                        "enable_ib",
                        "name"]
    __detach_flag = '--detach'
    __interactive_flag = '-it'
    __security_flag = '--security-opt=no-new-privileges'
    # TODO: check ib_devices
    __ib_devices = ["--device=/dev/infiniband/uverbs0", "--device=/dev/infiniband/rdma_cm"]

    __limits = ["--ulimit memlock=-1:-1"]

    def __init__(self, **kwargs):

        self.__image = kwargs.pop("image")

        if kwargs['interactive'] is False:
            self.__type = self.__detach_flag
        else:
            self.__type = self.__interactive_flag
        kwargs.pop("interactive")
        for key in kwargs.keys():
            if key not in self.__available_args:
                raise AttributeError("Incorrect parameters. "
                                     "Some args not available")

        self.__kwargs = kwargs

    @property
    def run_command(self):
        """
        :return:
        """
        command = ["docker", "run"]

        command.append("%s" % self.__type)
        command.append("%s" % self.__security_flag)

        command.extend(self.__ib_devices)
        command.extend(self.__limits)

        command.extend(volumes_to_list(self.__kwargs["volumes"]))
        self.__kwargs.pop("volumes")

        command.append("-P")
        command.extend(dict_to_list(self.__kwargs))

        command.append("%s" % self.__image)
        return command

    @staticmethod
    def remove_command(cont_name):
        """
        :return:
        """
        return ["docker", "rm", cont_name]

    @staticmethod
    def stop_command(cont_name):
        """
        :return:
        """
        return ["docker", "stop", cont_name]

    @staticmethod
    def print_available_kwargs():
        print(Container.__available_args)

    @staticmethod
    def exec_command(container_name, command):
        pattern = """docker exec -d %s sh -c "%s" """
        return pattern % (container_name, command)

    @staticmethod
    def img_from_cont(cont_name):
        """
        :param cont_name:
        :return:
        """
        return "docker ps -a --filter=name=%s --format='{{.Image}}'" % cont_name

    @staticmethod
    def remove_image(image):
        return ["docker", "rmi", image]


if __name__ == '__main__':
    c = Container(image="newmpich:latest", name="name", volumes="/usr:/usr /bin:/bin",
                  hostname="host", user="3333:1010", detach=True)
    print(c.run_command)
    print(c.remove_command)
    print(Container.remove("name"))

    print(Container.exec_command("mpi_ivan_133", "mpirun -np 3 --hostfile hst ./program -a a1 -b b1"))
