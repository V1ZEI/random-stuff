import socket


listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# listener.setsockopt(level, optname, value)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

listener.bind(("<Local IP>", port_number))
listener.listen(0)
print("[+] Waiting for a connection")
connection, address = listener.accept()
print("[+] Got a connection")

while True:
  input_command = input(">>> ")
  connection.send(input_command.encode('utf-8'))
  result = connection.recv(1024).decode('utf-8')
  print(result)
