"""
"""
import paramiko


def run_user_command(task_id, host, command):
    """"""
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(host)

    stdin, stdout, stderr = ssh_client.exec_command()

    ssh_client.close()
