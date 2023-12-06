import sys
import threading
import socket
import time
import struct
import concurrent.futures

class Node:

    neighbours = [] #(address:port)
    ip_rp = ""
    streaming_content = {} # (content_name, receiving_socket)
    nodes_requesting_content = {} # {content_name: [requesting_node_socket]}
    rp_neighbour = False
    path_to_rp = [] # List of nodes in the path to the RP (IP Only, the port will always be 50000)
    
    def main(self):
        print("Starting Node...")
        try:
            NODE_PORT = int(sys.argv[1])
            NODE_NUMBER = int(sys.argv[2])
            RP_NODE = sys.argv[3]
        except (IndexError, ValueError):
            print("[Usage: Node.py node_port node_number rp_ip]\n")

        self.read_ips_from_file(NODE_NUMBER)
        
        self.ip_rp = RP_NODE

        print(self.neighbours)
        # Check if we are connected to the RP and if so set rp_neighbour to True
        if self.ip_rp in self.neighbours:
            self.rp_neighbour = True

        # 1. Create a permanent listening loop for the RTSP socket
        nodeServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        nodeServerSocket.bind(('0.0.0.0', NODE_PORT))
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
            print(f"Sent new server port to {requesting_address}")

            # 4. Create a new thread to handle the client
            threading.Thread(target=self.handle_request, args=(new_server_port, requesting_address, request)).start()

            # 5. Close the socket
            requesting_socket.close()



    def read_ips_from_file(self, NODE_NUMBER):
        # Reads the IPs of the neighboring nodes, one IP per line
        filename = "node" + str(NODE_NUMBER) + ".txt"
        with open(filename) as f:
            for line in f:
                ip_address = line.strip()
                if ip_address:
                    self.neighbours.append(ip_address)




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
        print(f"Handling request from {requesting_address}")
        
        receiving_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        receiving_socket.bind(('0.0.0.0', new_server_port))
        print(f"Listening on port {new_server_port}")
        
        receiving_socket.listen(1)  # Make the socket a listening socket with a backlog of 1 connection
        
        requesting_node_socket, requesting_node_address = receiving_socket.accept() 


        # 1. Check the request type
        request_type = request.split(";;")[0]
        content_name = request.split(";;")[1]
        if request_type == "CONTENT_REQUEST":
            
            self.client_request(requesting_node_address, requesting_node_socket, content_name)

        # A logica aqui nao esta bem, isto nao funciona em casos de maior profundidade
        elif request_type == "LOCATE_RP":
            self.locate_rp(requesting_node_socket, content_name, request)

        elif request_type == "REDIRECT_REQUEST":
            self.redirect_request(requesting_node_socket, request)

        else:
            print(f"Invalid request: {request}")

       
        receiving_socket.close()  # Close the listening socket when done


        
    def client_request(self, requesting_node_address, requesting_node_socket, content_name):
        print(f"Requesting content from {requesting_node_address}")

        # 1. Check if the node is currently streaming the content
        if content_name in self.streaming_content:
            print("Node has the content")
            self.redirect_multicast(requesting_node_socket, content_name)

        # 2. If not, check if we are connected to the RP
        elif self.rp_neighbour:
            print("Node is connected to the RP")
            # 2.1. If so, send the request to the RP
            self.send_request_to_rp(content_name, requesting_node_socket)

        # 3. If not, locate the RP
        else:
            # print("Node is not connected to the RP")
            # # 3.1. Send a request to the neighbours to locate the RP
            # self.locate_rp(requesting_node_address, requesting_node_socket)
            # # 3.2. Request the content from the RP through the connected neighbour
            # self.send_request_to_neighbour(content_name, requesting_node_socket, connected_neighbour) 
            pass


    # Stream already exists, redirect the requesting node to the multicast group
    def redirect_multicast(self, request_socket, content_name):
        # Send the message MULTICAST_STREAM to the requesting node
        response_msg = f"MULTICAST_STREAM;;{content_name}"
        request_socket.send(response_msg.encode())
        time.sleep(1)
        print(f"Already streaming {content_name}, redirecting content to the requesting node")
        # Simply add the requesting node to the list of nodes requesting the content
        self.nodes_requesting_content[content_name].append(request_socket)
            

    # Send a request to the RP to get a stream of the content
    def send_request_to_rp(self, content_name, requesting_socket):
        # Create a socket to connect to the RPNode
        node_to_rp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the RPNode
        node_to_rp_socket.connect((self.ip_rp, 5000))

        # Send a CONTENT_REQUEST
        request_msg = f"CONTENT_REQUEST;;{content_name}"
        node_to_rp_socket.send(request_msg.encode())
        print(f"Sent CONTENT_REQUEST to the RPNode at {self.ip_rp}:{5000} for content: {content_name}")

        # Receive the response from the RPNode
        new_port = node_to_rp_socket.recv(1024).decode()
        print(f"Received response from the RPNode: {new_port}")

        # Close the initial socket
        node_to_rp_socket.close()

        time.sleep(2)

        # Connect to the new NodeRP port to get the stream
        receiving_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("connecting to the new port " + new_port)
        receiving_socket.connect((self.ip_rp, int(new_port)))
        time.sleep(1)

        print("waiting for response")
        while True:
            response_bytes = receiving_socket.recv(1024)
            response = response_bytes.decode()
            print(f"Received response from the RPNode: {response}")
            if response.startswith("MULTICAST_STREAM"):
                self.streaming_content[content_name] = receiving_socket
                self.nodes_requesting_content[content_name] = [requesting_socket]
                self.receive_stream(receiving_socket, content_name)
            else:
                print("content not found")
                break
                
        print("Exited the loop")  # Add this line to check if the loop is exited
        receiving_socket.close()  # Close the new_socket after exiting the loop


    # Receive the stream from the RP and redirect it to the requesting node
    def receive_stream(self, receiving_socket, content_name):
        # Receive each packet of data from the server and redirect it to the requesting node
        while True:
            data, addr = receiving_socket.recvfrom(20480)
            if data:
                for node in self.nodes_requesting_content[content_name]:
                    node.send(data[:])
            if not data:
                self.streaming_content.pop(content_name)
                # Close the socket  
                receiving_socket.close()
                print("Exiting")
                break



    # Function to handle LOCATE_RP request for a single neighbour
    def handle_neighbour(self, neighbour_ip, request, requesting_node_socket, response_path):
        # Check if the neighbour's IP is already in the response path
        if neighbour_ip in response_path:
            print(f"Skipping neighbour {neighbour_ip} as it is already in the response path")
            return

        # Create a socket to connect to the neighbour
        node_to_neighbour_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the neighbour
        node_to_neighbour_socket.connect((neighbour_ip, 5000))

        # Send the request to the neighbour
        node_to_neighbour_socket.send(request.encode())
        print(f"Sent LOCATE_RP request to the neighbour at {neighbour_ip}:{5000}")

        # Receive the response from the neighbour
        response = node_to_neighbour_socket.recv(1024).decode()
        print(f"Received response from neighbour at {neighbour_ip}:{5000}: {response}")

        # Process the response (you might want to add more logic here)
        # For now, send the response to the requesting node
        response_msg = f"PATH_TO_RP;;{response};;{self.ip_rp}"
        requesting_node_socket.send(response_msg.encode())
        print(f"Sent PATH_TO_RP response to the node for the content")

        # Close the socket after sending/receiving the response
        node_to_neighbour_socket.close()

    # Send a request to the neighbours to locate the RP
    # And handle the response from the neighbours
    def locate_rp(self, requesting_node_socket, content_name, request):
        separator = ";;"
        request_path = request.split(separator, 1)[1]

        if self.rp_neighbour:
            # Send a PATH_TO_RP message to the requesting node with the path to this node
            response_msg = f"PATH_TO_RP;;{request_path};;{self.ip_rp}"
            requesting_node_socket.send(response_msg.encode())
            print(f"Sent PATH_TO_RP response to the node for the content: {content_name}")

        else:
            # Send a LOCATE_RP request to the neighbours using threads
            print("Sending LOCATE_RP request to the neighbours")

            # Use ThreadPoolExecutor to submit threads for each neighbour
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []

                for neighbour_ip in self.neighbours:
                    threaded_request = request + f";;{neighbour_ip}"
                    future = executor.submit(self.handle_neighbour, neighbour_ip, threaded_request, requesting_node_socket, request_path)
                    futures.append(future)

                # Wait for the first thread to complete and get its result
                for future in concurrent.futures.as_completed(futures):
                    # Break after the first completed thread
                    break

    # Vai encaminhar os pacotes recebidos para o node seguinte no caminho recebido no pacote, acrescentando 1 ao contador de hops
    def redirect_request(self, requesting_node_socket, request):
        pass

    def send_request_to_neighbour(self, content_name, requesting_socket, connected_neighbour):
        pass

    # Vai encaminhar o pedido para o node seguinte no caminho para o RP acrescentando 1 ao contador de hops
    # O ultimo nodo sera responsavel por enviar o pedido ao RP
    def request_stream(self, requesting_address, socket, request):
        pass



if __name__ == "__main__":
    (Node()).main()
