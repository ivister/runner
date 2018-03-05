import os
import paramiko

host = '192.168.1.33'
port = 22

if __name__ == '__main__':
    command = "ssh 192.168.1.33"
    second = "docker images"

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, port=port)
    stdin, stdout, stderr = client.exec_command(second)
    data = stdout.read() + stderr.read()
    print(data.decode())

    print("here")
    stdin.flush()

    stdout.flush()
    stderr.flush()
    stdin, stdout, stderr = client.exec_command("docker run -d hello-world")
    data = stdout.read() + stderr.read()

    print(data.decode())
    client.close()