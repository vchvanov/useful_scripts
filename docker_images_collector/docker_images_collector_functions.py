#!/usr/bin/python3

import sys
import time

from scp import SCPClient
import paramiko

def ssh_connect_cmd(ip,port,username,password,timeout,cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port, username=username, password=password, timeout=timeout)

    stdin, stdout, stderr = client.exec_command(cmd)
    exit_status = stdout.channel.recv_exit_status()

    if exit_status != 0:
        print("Error", exit_status)

    client.close()

    return stdin, stdout, stderr

def progress(filename, size, sent):
    sys.stdout.write("%s's progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100))

def ssh_scp_get(ip,port,username,password,timeout,file):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port, username=username, password=password, timeout=timeout)

    scp = SCPClient(client.get_transport(), progress=progress)
    scp.get(file, local_path=sys.path[0])
    scp.close()
