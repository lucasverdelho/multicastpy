import sys
import socket
from ServerWorker import ServerWorker
import threading

class Node:
    

    neighbours = []
    rp_node_ip = "0.0.0.0"

    def main(self):
        try:
            NODE_PORT = int(sys.argv[1])
            NODE_NUMBER = int(sys.argv[2])
        except (IndexError, ValueError):
            print("[Usage: Node.py node_port node_number]\n")

        self.neighbours = self.read_ips_from_file()

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

    def read_ips_from_file(self):
        with open('neighbours.txt') as f:
            for line in f:
                self.neighbours.append

    def handle_request(self, request_socket, request_address):
        request = request_socket.recv(1024).decode()
        print(f"Received request: {request}")

        if request == "CONTENT_REQUEST":
            self.handle_content_request(request, request_socket, request_address)
        elif request == "LOCATE_RP_REQUEST":
            self.handle_locate_request(request, request_socket, request_address)
        else:
            print("Invalid request.")


    def handle_content_request(self, request, request_socket, request_address):
        
        print("Handling content request...")
        
        content_requested = request.split(";")


        

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



if __name__ == "__main__":
    (Node()).main()



####### TODO
# 1. Read from file the neighbor nodes ips