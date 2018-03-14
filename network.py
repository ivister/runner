"""
"""

from functions import dict_to_string


class EthernetNetwork(object):
    """
    """
    __available_args = ["driver",
                        "subnet",
                        "gateway",
                        "ip_range",
                        "attachable",
                        "name"]
    __attachable_flag = "--attachable"

    def __init__(self, **kwargs):

        self.__name = kwargs.pop("name")
        if "attachable" in kwargs.keys():
            self.__is_attachable = kwargs.pop("attachable")

        for key in kwargs.keys():
            if key not in self.__available_args:
                raise AttributeError("Incorrect parameters. "
                                     "Some args not available")

        self.__kwargs = kwargs
        pass

    def get_name(self):
        return self.__name

    @property
    def create_command(self):
        """
        :return:
        """
        command = "docker network create %s" % dict_to_string(self.__kwargs)

        if hasattr(self, "__is_attachable"):
            command += " %s" % self.__attachable_flag
        command += " %s" % self.__name
        return command

    @property
    def remove_command(self):
        """
        :return:
        """
        return "docker network rm %s" % self.__name

    @staticmethod
    def print_available_kwargs():
        print(EthernetNetwork.__available_args)

    @staticmethod
    def remove(name):
        """
        :param name:
        :return:
        """
        return "docker network rm %s" % name


if __name__ == '__main__':
    o = EthernetNetwork(attachable=True, gateway="haha_gw",
                        name="my_net", driver="overlay", subnet="subnet")
    print(o.create_command)
    print(o.remove_command)
    print(EthernetNetwork.remove("my_net"))
