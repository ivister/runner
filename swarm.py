"""
"""
from default import DEFAULT_ADAPTER


class Swarm(object):
    """
    """
    def __init__(self):
        pass

    @staticmethod
    def init_swarm(ssh_client, eth_adapter=DEFAULT_ADAPTER):
        join_command = "docker swarm init --advertise-addr=%s" % eth_adapter
        _, stdout, stderr = ssh_client.exec_command(join_command)
        token = Swarm.get_token_from_out(stdout.read())
        stdout.flush()
        stderr.flush()
        return token

    @staticmethod
    def connect_to_swarm(ssh_client, token):
        _, _, stderr = ssh_client.exec_command(token)
        stderr.read()
        stderr.flush()

    @staticmethod
    def get_token_from_out(encoded_out):
        data = encoded_out.decode()
        sentences = data.split("\n")
        token = sentences[4].lstrip()
        return token

    @staticmethod
    def get_leave_command():
        return "docker swarm leave --force"


if __name__ == '__main__':
    print(Swarm.get_leave_command())
