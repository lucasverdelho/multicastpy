import socket
import threading
import json
import sys

class Node:
    def __init__(self, node_id, config_file):
        self.node_id = node_id
        self.connections = set()
        self.server_socket = None
        self.load_config(config_file)

    def load_config(self, config_file):
        with open(config_file, 'r') as file:
            config_data = json.load(file)
            self.connect_to_nodes(config_data['connected_nodes'])

    def connect_to_nodes(self, nodes):
        for node_ip in nodes:
            if node_ip != self.node_id:
                self.connect_to_node(node_ip)

    def connect_to_node(self, node_ip):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((node_ip, 5000))
            self.connections.add(client_socket)
            print(f"Connected to {node_ip}")
        except Exception as e:
            print(f"Error connecting to {node_ip}: {e}")

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', 5000))
        self.server_socket.listen(5)
        print(f"Node {self.node_id} is listening for connections.")

        while True:
            client_socket, addr = self.server_socket.accept()
            self.connections.add(client_socket)
            print(f"Node {self.node_id} accepted connection from {addr}")

            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            for connection in self.connections:
                if connection != client_socket:
                    connection.sendall(data)

        self.connections.remove(client_socket)
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <node_id>")
        sys.exit(1)

    node_id = sys.argv[1]
    config_file = f"config_{node_id}.json"

    node = Node(node_id, config_file)

    threading.Thread(target=node.start_server).start()

    while True:
        pass
