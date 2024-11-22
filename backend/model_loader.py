import paramiko
import os

def ssh_connect(host, user, key_path):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, key_filename=key_path)
    return ssh

def load_model(ssh, model_path):
    command = f"./llama.cpp --load {model_path}"
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read(), stderr.read()
