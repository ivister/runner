"""
"""

from functions import dict_to_string


class EthernetNetwork(object):
    """
    """
    available_args = ["driver",
                      "subnet",
                      "gateway",
                      "ip_range",
                      "attachable",
                      "name"
                      ]
    __attachable_flag = "--attachable"

    def __init__(self, **kwargs):

        self.__name = kwargs["name"]
        self.__is_attachable = kwargs["attachable"]

        for key in kwargs.keys():
            if key not in self.available_args:
                raise AttributeError("Incorrect parameters. Some args not available")

        self.__kwargs = kwargs
        self.__kwargs.pop("attachable")
        self.__kwargs.pop("name")
        pass

    @property
    def create_command(self):
        command = "docker network create %s" % dict_to_string(self.__kwargs)

        if self.__is_attachable:
            command += " %s" % self.__attachable_flag
        command += " %s" % self.__name
        return command

    @property
    def remove_command(self):
        return "docker network rm %s" % self.__name

    @staticmethod
    def remove(name):
        return "docker network rm %s" % name


if __name__ == '__main__':
    o = EthernetNetwork(attachable=True, gateway="haha", name="my_net", driver="overlay", subnet="subnet")
    print(o.create_command)
    print(o.remove_command)
    print(EthernetNetwork.remove("my_net"))
