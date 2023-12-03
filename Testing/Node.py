import sys
import threading
import socket

class Node:

    neighbours = [] #(address:port)
    ip_rp = "0.0.0.0:5000"
    streaming_content = {} # (content_name, receiving_socket)
    rp_neighbour = False

    
    def main(self):
        print("Starting Node...")
        try:
            NODE_PORT = int(sys.argv[1])
            NODE_NUMBER = int(sys.argv[2])
        except (IndexError, ValueError):
            print("[Usage: Node.py node_port node_number]\n")

        self.neighbours = self.read_ips_from_file(NODE_NUMBER)
        
        # Check if we are connected to the RP and if so set rp_neighbour to True
        if self.ip_rp in self.neighbours:
            self.rp_neighbour = True

        # 1. Create a permanent listening loop for the RTSP socket
        nodeServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        nodeServerSocket.bind(('', NODE_PORT))
        nodeServerSocket.listen(5)

        # MAIN LISTEN LOOP
        # Cria uma nova thread para cada requesição
        while True:

            # 2. Wait for any connection request
            requesting_socket, requesting_address = nodeServerSocket.accept()
            print(f"Requesting socket connected: {requesting_address}")

            request = requesting_socket.recv(1024).decode()

            # 3. Create new port for the new communication socket and send it back to the requesting node
            new_server_port = self.find_available_port()
            print(f"New server port: {new_server_port}")
            response_msg = f"{new_server_port}"
            requesting_socket.send(response_msg.encode())

            # 4. Create a new thread to handle the client
            threading.Thread(target=self.handle_request, args=(new_server_port, requesting_address, request)).start()

            # 5. Close the socket
            requesting_socket.close()



    def read_ips_from_file(self, NODE_NUMBER):
        #reads the ips of the neighnouring nodes
        filename = "node" + NODE_NUMBER + ".txt"
        with open(filename) as f:
            for line in f: #each line will be the ip of the neighnours
                self.neighbours.append()


    def find_available_port(self):
        try:
            temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            temp_socket.bind(('localhost', 0))  # Bind to an available port on localhost
            temp_socket.listen(1)
            port = temp_socket.getsockname()[1]
            temp_socket.close()
            return port
        except socket.error:
            print("Error finding available port.")
            return None


    def handle_request(self, new_server_port, requesting_address, request):

        socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.connect((requesting_address, new_server_port))


        if request == "CONTENT_REQUEST":
            self.content_request(requesting_address, socket)
        elif request == "LOCATE_RP":
            self.locate_rp(requesting_address, socket)
        else:
            print(f"Invalid request: {request}")
        

    def content_request(self, requesting_address, socket):
        print(f"Requesting content from {requesting_address}")
        # 1. Receive the content name
        content_name = socket.recv(1024).decode()
        print(f"Content name: {content_name}")

        # 2. Check if the node has the content
        if content_name in self.streaming_content:
            print("Node has the content")

        # 3. If not, check if we are connected to the RP
        elif self.rp_neighbour:
            print("Node is connected to the RP")
            # 3.1. If so, send the request to the RP
            self.send_request_to_rp(content_name, socket)

        # 4. If not, locate the RP
        else:
            print("Node is not connected to the RP")
            # 4.1. Send a request to the neighbours to locate the RP
            self.locate_rp(requesting_address, socket)

        
        def locate_rp(self, requesting_address, socket):
            print(f"Locating RP from {requesting_address}")
            # 1. Send a request to the neighbours to locate the RP
            for neighbour in self.neighbours:
                # 1.1. Create a new socket to send the request
                neighbour_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                neighbour_socket.connect(neighbour)
                # 1.2. Send the request
                neighbour_socket.send("LOCATE_RP".encode())
                # 1.3. Wait for the response
                response = neighbour_socket.recv(1024).decode()
                


            


if __name__ == "__main__":
    (Node()).main()
