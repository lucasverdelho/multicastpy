import sys
import socket
import threading



class NodeClientWorker:
    def main(self, master):


            

    if __name__ == "__main__":
    (Node()).main()


import socket
import threading

class ServerClient:
    def __init__(self, port):
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', port))
        self.server_socket.listen(1)
        self.client_socket = None

    def start_server(self):
        print(f"Server listening on port {self.port}")
        while True:
            self.client_socket, client_address = self.server_socket.accept()
            print(f"Accepted connection from {client_address}")
            threading.Thread(target=self.receive_data).start()

    def start_client(self, server_address, server_port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_address, server_port))
        threading.Thread(target=self.receive_data).start()

    def send_data(self, message):
        if self.client_socket:
            self.client_socket.send(message.encode())
        else:
            print("Not connected to a server.")

    def receive_data(self):
        while True:
            data = self.client_socket.recv(1024)
            if not data:
                break
            print(f"Received: {data.decode()}")

    def stop(self):
        if self.client_socket:
            self.client_socket.close()
        if self.server_socket:
            self.server_socket.close()

# Example usage:
# Create an instance and start the server
server_client = ServerClient(12345)
threading.Thread(target=server_client.start_server).start()

# Create another instance and start the client
client = ServerClient(0)  # 0 for dynamic port assignment
client.start_client('localhost', 12345)

# Send data from the client to the server
client.send_data("Hello from the client!")

# Send data from the server to the client
server_client.send_data("Hello from the server!")

# Clean up
server_client.stop()
client.stop()
