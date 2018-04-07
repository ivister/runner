"""
"""
from default import DEFAULT_ADAPTER

class Swarm(object):
    """
    """
    def __init__(self):
        pass

    @staticmethod
    def init_swarm(ssh_client, , eth_adapter=DEFAULT_ADAPTER):
        join_command = "docker swarm init --advertise-addr=%s"
        _, stdout, stderr = ssh_client.exec_command(join_command)
        token = Swarm.get_token_from_out(stdout.read())
        pass

    @staticmethod
    def get_token_from_out(encoded_out):
        data = decoded_out.decode()
        sentences = data.split("\n")
        tocken = sentences[4]
        print(token)
        pass
