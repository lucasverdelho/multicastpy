import socket
import threading
import time

class Node:
    def main(self, node_id, port):
        self.node_id = node_id
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', port))
        self.sock.listen(5)
        
        self.connections = {}  # Dictionary to store connected nodes (node_id: socket)

        self.start()

    def accept_connections(self):
        while True:
            client_socket, client_address = self.sock.accept()
            node_id = client_socket.recv(1024).decode()
            self.connections[node_id] = client_socket
            print(f"Node {self.node_id} connected to Node {node_id} at {client_address}")

    def connect_to_node(self, other_node_id, other_node_port):
        #connects to neighbours | prepares to send data
        other_node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        other_node_socket.connect(('localhost', other_node_port))
        other_node_socket.send(str(self.node_id).encode())
        self.connections[other_node_id] = other_node_socket
        print(f"Node {self.node_id} connected to Node {other_node_id}")

    def send_message(self, dest_node_ids, message):
        for dest_node_id in dest_node_ids:
            dest_socket = self.connections.get(dest_node_id)
            if dest_socket:
                try:
                    dest_socket.send(message.encode())
                except:
                    print(f"Error sending message to Node {dest_node_id}")

    def receive_messages(self):
        while True:
            for node_id, socket in list(self.connections.items()):
                try:
                    data = socket.recv(1024)
                    if not data:
                        print(f"Node {self.node_id} disconnected from Node {node_id}")
                        del self.connections[node_id]
                    else:
                        print(f"Received from Node {node_id}: {data.decode()}")
                except:
                    print(f"Node {self.node_id} disconnected from Node {node_id}")
                    del self.connections[node_id]

    def start(self):
        threading.Thread(target=self.accept_connections).start()
        threading.Thread(target=self.receive_messages).start()

    def stop(self):
        for client_socket in self.connections.values():
            client_socket.close()
        if self.sock:
            self.sock.close()


    if __name__ == "__main__":
    (Node()).main()