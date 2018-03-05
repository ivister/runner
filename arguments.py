"""
"""


class RunArguments(object):
    """
    """
    """EXAMPLE:
        docker run -d
        --name=docker_SuppzJobId
        --hostname
        -v /usr:/usr
        -v /ex:/ex
        -v /ex2:/ex2
        ...
        main/user_image:latest
    """

    def __init__(self, volumes, device, name, user, hostname, image_name):
        self.__volumes = volumes.split(" ")
        self.__device = device
        self.__name = name
        self.user = user
        self.hostname = hostname
        self.image_name = image_name

    def __str__(self):
        res = "--device=" + self.__device + " --name=" + self.__name + " --hostname=" + self.hostname
        for v in self.__volumes:
            res += " -v " + v
        return res


if __name__ == '__main__':
    te = RunArguments(name="docker_123123", device="/dev/infiniband/uverbs0", user="Alex:users",
                   hostname="node00", image_name="test/ib_image:latest", volumes="/etc:/etc /usr:/usr")
    print(te)