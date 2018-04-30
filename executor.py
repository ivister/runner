"""
"""
import paramiko
from container import Container


def run_user_command(task_id, host, command):
    """"""
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(host)
    cont_name = "%s-%s" % (host, task_id)
    _, _, _ = ssh_client.exec_command(Container.exec_command(container_name=cont_name, command=command))
    # err = stderr.read()
    # print(err)

    ssh_client.close()
