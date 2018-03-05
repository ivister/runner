"""

"""
from arguments import RunArguments, LoadArguments, StopArguments


class DockerCommand(object):
    """
    """
    Run = 1
    Load = 2
    Stop = 9
    Kill = 10

    def __init__(self, command_type, arguments):
        if command_type == self.Run:
            self.__prefix = "docker run "
            if not isinstance(arguments, RunArguments):
                raise AttributeError('Invalid Arguments. Invalid arguments type.')
            pass
        elif command_type == self.Load:
            self.__prefix = "docker load "
            if not isinstance(arguments, LoadArguments):
                raise AttributeError('Invalid Arguments. Invalid arguments type.')
            pass
        elif command_type == self.Stop:
            self.__prefix = "docker stop "
            if not isinstance(arguments, StopArguments):
                raise AttributeError('Invalid Arguments. Invalid arguments type.')
            pass
        elif command_type == self.Kill:
            self.__prefix = "docker kill "
        else:
            raise AttributeError('Invalid Arguments. Unknown command type.')

        self.parameters = arguments.__str__()

    def __str__(self):
        return self.__prefix + self.parameters

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    args = RunArguments(name="docker_123123",
                        device="/dev/infiniband/uverbs0",
                        user="Alex:users",
                        hostname="node00",
                        image_name="test/ib_image:latest",
                        volumes="/etc:/etc /usr:/usr")
    cm = DockerCommand(command_type=DockerCommand.Run, arguments=args)

    print(cm)