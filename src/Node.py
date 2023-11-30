import sys
import socket
from ServerWorker import ServerWorker
import threading

class Node:
    

    neighbours = []
    streaming_content = {}
    rp_node_ip = "0.0.0.0:5000"

    def main(self):
        try:
            NODE_PORT = int(sys.argv[1])
            NODE_NUMBER = int(sys.argv[2])
        except (IndexError, ValueError):
            print("[Usage: Node.py node_port node_number]\n")

        self.neighbours = self.read_ips_from_file(NODE_NUMBER)

        nodeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        nodeSocket.bind(('', NODE_PORT))
        nodeSocket.listen(5)


        local_address = nodeSocket.getsockname()
        print(local_address)

        while True:
            request_socket, request_address = nodeSocket.accept()
            print(f"Request connected: {request_address}")

            self.handle_request(request_address, request_socket)

            request_socket.close()            

    def read_ips_from_file(self, NODE_NUMBER):
        filename = "node" + NODE_NUMBER + ".txt"

        with open(filename) as f:
            for line in f:
                self.neighbours.append

    def handle_request(self, request_socket, request_address):
        request = request_socket.recv(1024).decode()
        print(f"Received request: {request}")

        if request == "CONTENT_REQUEST":
            threading.Thread(target=self.handle_content_request, args=(request, request_socket, request_address)).start()
        elif request == "LOCATE_RP_REQUEST":
            threading.Thread(target=self.handle_locate_request, args=(request, request_socket, request_address)).start()
        else:
            print("Invalid request.")

        return

    def handle_content_request(self, request, request_socket, request_address):
        
        print("Handling content request...")
        
        content_requested = request.split(";")

        if self.streaming_content.contains(content_requested):
            # Copy each packet of data from the stream to the request socket
            


        # Check if the node is connected to the RP
        if self.neighbours.contains(self.rp_node_ip):
            print("Node is connected to the RP.")
            self.send_content_request(content_requested, request_socket, request_address)


        # Send Request to RP for the content
        # TODO 
        # 1. Create socket to handle the request propagation
        # 2. Listen for the response of a Node who has the content
        #

    def handle_locate_request(self, request, request_socket, request_address):
        print("Handling locate request...")

        # Send Request to RP for the content
        # TODO 
        # 1. Create socket to handle the request propagation
        # 2. Listen for the response of a Node who is neighbour to the RP



    def send_content_request(self, content_requested, request_socket, request_address):
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        temp_socket.connect((self.rp_node_ip, 5000))
        request = "CONTENT_REQUEST;" + content_requested
        temp_socket.send(request.encode())

        

if __name__ == "__main__":
    (Node()).main()



####### TODO
# 1. Read from file the neighbor nodes ips