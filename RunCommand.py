"""

"""
from arguments import RunArguments


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
        elif command_type == self.Load:
            pass
        elif command_type == self.Stop:
            pass
        else:
            raise ValueError('Invalid Arguments. Unknown command type.')

        if type(arguments) is not type(RunArguments):
            print(type(arguments))
            print(type(arguments.RunArguments))
            raise ValueError('Invalid Arguments. Invalid arguments type.')

    def __str__(self):
        return self

if __name__ == '__main__':
    args = RunArguments(name="docker_123123",
                        device="/dev/infiniband/uverbs0",
                        user="Alex:users",
                        hostname="node00",
                        image_name="test/ib_image:latest",
                        volumes="/etc:/etc /usr:/usr")

    cm = DockerCommand(command_type=DockerCommand.Run, arguments=args)
