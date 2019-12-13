import paramiko
import os


class FTP:
    def __init__(self, username, pwd, port):
        global sftp
        global ssh_cmd
        global tran
        host_name = "35.223.248.16"
        tran = paramiko.Transport((host_name, port))
        tran.connect(username=username, password=pwd)
        sftp = paramiko.SFTPClient.from_transport(tran)
        ssh_cmd = paramiko.SSHClient()
        ssh_cmd.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_cmd.connect(host_name, 22, username, pwd)

    def uploader(self, client_path, server_path):
        sftp.put(client_path, server_path)
        return

    def create_new_folder(self, server_path):
        cmd = 'mkdir %s' % server_path
        ssh_cmd.exec_command(cmd)
        return

    def disconnect(self):
        ssh_cmd.close()
        sftp.close()
        tran.close()
        return




