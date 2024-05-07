#!/usr/bin/python3

import os
import socket
import sys
import time
import paramiko
from datetime import datetime
from pathlib import Path
from shutil import copyfile
from docker_images_collector_functions import ssh_connect_cmd, ssh_scp_get

# Script is executable once a week in cron and it's saved to the log file
#
# At the beginning of the script we're checking :
#
# 1. if the log file is greater than 50 Mb and deleting it if it does
# 2. if directory, where backups will be stored, exists and create it if not
# 3. if files in directory, where backups will be stored, older than 3 weeks and deleteing it if it does

os.system("echo Starting script docker_images_collector\r\n")
os.system('sudo find /home/harmonic/cronlog/docker_images_collector/docker_images_collector_cron.log -size +50M -exec rm -rf {} +')
Path('/var/www/html/docker_backups/').mkdir(parents=True, exist_ok=True)
os.system('sudo find /var/www/html/docker_backups -mtime +21 -exec rm -rf {} +')

print('Start time: ', datetime.now(), '\n')

timestamp = time.strftime("%Y%m%d")

# Open the hosts file, which stores all data regarding setup VM, and parse it to the list

with open(os.path.join(sys.path[0], "docker_images_collector_hosts.txt"), "r") as my_file:
    for line in my_file:
        setup_name, host, port, username, password = line.split()
        print('\n\nStarting backup for ACM {host} of setup {setup_name}'.format(**locals()))

        for attempt in range(3):
            try:

                # Retrieve container id and image for the setup container

                cmd = "docker ps | awk '{if ($NF == \"" + setup_name + "\") print $1}'"
                fin, fout, ferr = ssh_connect_cmd(host, port, username, password, 10, cmd)
                fin.close()
                containerid_list = fout.readlines()

                containerid_string = ' '.join([item.strip() for item in containerid_list])
                print('Container Id for commit : ', containerid_string)


                cmd = "docker ps | awk '{if ($NF == \"" + setup_name + "\") print $2}'"
                fin, fout, ferr = ssh_connect_cmd(host, port, username, password, 10, cmd)
                fin.close()
                image_list = fout.readlines()

                image_string = ' '.join([item.strip() for item in image_list])
                image = image_string + "_" + setup_name + "_" + timestamp
                print('Image for backup : ', image)

                # Perform commit to have image with all changes

                cmd = "docker commit " + containerid_string + " " + image
                fin, fout, ferr = ssh_connect_cmd(host, port, username, password, 10, cmd)
                fin.close()

                print('Commit done!')

                # Saving recieved image to tar archieve

                cmd = "docker image save -o " + setup_name + "_docker_images_backup.tar " + image
                fin, fout, ferr = ssh_connect_cmd(host, port, username, password, 10, cmd)
                fin.close()

                print('Image backed up!', '\nBackup saved on the ACM {host} in /home/ubuntu/'.format(**locals()))

                # Deleting image

                cmd = "docker image rm " + image
                fin, fout, ferr = ssh_connect_cmd(host, port, username, password, 10, cmd)
                fin.close()

                print('Image deleted!')

                break

            except (paramiko.ssh_exception.BadHostKeyException, paramiko.ssh_exception.AuthenticationException,
             paramiko.ssh_exception.SSHException, socket.error) as e:
                print(e)
                time.sleep(10)
                continue

        # Renaming file with adding to it the timestamp (day, month, year)

        file = setup_name + "_docker_images_backup.tar"
        new_file = setup_name + "_docker_images_backup_" + timestamp + ".tar"

        # Downloading tar backup to the local machine and copy of it to the final directory (Apache)

        for attempt in range(3):
            try:
                ssh_scp_get(host, port, username, password, 10, file)
                print('Backup saved on local machine')

                cmd = 'rm -rf ' + setup_name + "_docker_images_backup.tar"
                ssh_connect_cmd(host, port, username, password, 10, cmd)

                src = os.path.join(sys.path[0], file)
                dst = '/var/www/html/docker_backups/' + file
                copyfile(src, dst)

                os.system('sudo mv /var/www/html/docker_backups/' + file + ' /var/www/html/docker_backups/' + new_file)
                os.remove(os.path.join(sys.path[0], file))

                print('File moved to /var/www/html/docker_backups/')
                break

            except (paramiko.ssh_exception.BadHostKeyException, paramiko.ssh_exception.AuthenticationException,
             paramiko.ssh_exception.SSHException, socket.error) as e:
                print(e)
                time.sleep(10)
                continue

print('\nEnd time: ', datetime.now(), '\n\n')
