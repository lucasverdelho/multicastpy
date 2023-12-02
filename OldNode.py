import sys
import socket
from ServerWorker import ServerWorker

from NodeClientWorker import NodeClientWorker
from NodeServerWorker import NodeServerWorker

import threading

''''
    while True:
        clientInfo = {}
        clientInfo['rtspSocket'] = rtspSocket.accept()
        ServerWorker(clientInfo).run()
'''



class Node:
    
    neighbours = []
    streaming_content = [["movie.Mjepg", 2000, [2001]]] #itens: ["name_of_media", socket_receiving, socket_sending]
    
    default_server_side_port = 3000
    default_client_side_port = 4000

    rp_node_ip = "0.0.0.0:5000"


    def main(self):
        try:
            # NODE_PORT = int(sys.argv[1])    #default node port
            NODE_NUMBER = int(sys.argv[2])  #id of node
        except (IndexError, ValueError):
            print("[Usage: Node.py node_port node_number]\n")

        self.neighbours = self.read_ips_from_file(NODE_NUMBER)

        #default server socket | ports are 3000+i
        #this socket listen to receiving data
        nodeServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        nodeServerSocket.bind(('', default_server_side_port))
        nodeServerSocket.listen(5)



        #default client socket | ports are 4000 + i
        #this socket sends data
        nodeClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        local_client_socket_address = nodeClientSocket.getsockname()  #address of the node client-socket
        print(local_address)

        #handling of requests
        while True:
            request_socket, request_address = nodeSocket.accept()
            print(f"Request connected: {request_address}")
            self.handle_request(request_address, request_socket)
            request_socket.close()            

    def read_ips_from_file(self, NODE_NUMBER):
        #reads the ips of the neighnouring nodes
        filename = "node" + NODE_NUMBER + ".txt"
        with open(filename) as f:
            for line in f: #each line will be the ip of the neighnours
                self.neighbours.append()

    def handle_request(self, request_socket, request_address):
        #determines which type of request it is
        request = request_socket.recv(1024).decode()
        print(f"Received request: {request}")

        if request[0] == "CONTENT_REQUEST":
            threading.Thread(target=self.handle_content_request, args=(request, request_socket, request_address)).start()
        elif request[0] == "LOCATE_RP_REQUEST":
            threading.Thread(target=self.handle_locate_request, args=(request, request_socket, request_address)).start()
        else:
            print("Invalid request.")

    def handle_content_request(self, request, request_socket, request_address):
        #handles content requests depending if it is already streaming content to an ip
        print("Handling content request...")
        
        #format of content_requested should be ["name_of_media"]
        content_requested = request.split(";")

        if !self.is_streamed(content_requested):
            self.ask_content(request)
            self.send_stream(request_socket, request_address)
        else:
            self.new_scocket_existing_stream(request_socket, request_address)
            
            
        # Check if the node is connected to the RP
        #if self.neighbours.contains(self.rp_node_ip):
        #    print("Node is connected to the RP.")
        #    self.send_content_request(content_requested, request_socket, request_address)


        # Send Request to RP for the content
        # TODO 
        # 1. Create socket to handle the request propagation
        # 2. Listen for the response of a Node who has the content
        #

    def is_streamed(self, content_requested):
        #verifies if this node is streaming this content right now and returns the receiving socket of the content
        for streams in self.streaming_content:
            if streams[0] == content_requested:
                return streams[1]
        return false

    def send_stream(self, request_socket, request_address):


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