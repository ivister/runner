"""
"""

from functions import volumes_to_string
from functions import dict_to_string


class Container(object):
    """
    """
    __available_args = ["volumes",
                        "devices",
                        "hostname",
                        "user",
                        "image",
                        "detach",
                        "interactive",
                        "name"]
    __detach_flag = '--detach'
    __interactive_flag = '-i'
    __security_flag = '--security-opt=no-new-privileges'

    def __init__(self, **kwargs):

        self.__image = kwargs.pop("image")

        if "detach" in kwargs.keys():
            self.__type = self.__detach_flag
            kwargs.pop("detach")
        elif "interactive" in kwargs.keys():
            kwargs.pop("interactive")
            self.__type = self.__interactive_flag

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
        command = "docker run"
        command += " %s" % self.__security_flag

        command += " %s" % self.__type
        command += volumes_to_string(self.__kwargs["volumes"])
        self.__kwargs.pop("volumes")
        command += dict_to_string(self.__kwargs)

        command += " %s" % self.__image
        return command

    @property
    def remove_command(self):
        """
        :return:
        """
        return "docker rm %s" % self.__kwargs["name"]

    @property
    def stop_command(self):
        """
        :return:
        """
        return "docker stop %s" % self.__kwargs["name"]

    @staticmethod
    def print_available_kwargs():
        print(Container.__available_args)

    @staticmethod
    def remove(name):
        """
        :param name:
        :return:
        """
        return "docker rm %s" % name

    @staticmethod
    def stop(name):
        """
        :param name:
        :return:
        """
        return "docker stop %s" % name

    @staticmethod
    def img_from_cont(cont_name):
        """
        :param cont_name:
        :return:
        """
        return "docker ps -a --filter=name=%s --format='{{.Image}}'" % cont_name

    @staticmethod
    def remove_image(image):
        return "docker rmi %s" % image


if __name__ == '__main__':
    c = Container(image="newmpich:latest", name="name", volumes="/usr:/usr /bin:/bin", hostname="host", user="3333:1010", detach=True)
    print(c.run_command)
    print(c.remove_command)
    print(Container.remove("name"))