import sys
import threading
import socket

class Node:

    neighbours = [] #(address:port)
    ip_rp = "0.0.0.0:5000"
    streaming_content = {} # (content_name, receiving_socket)
    rp_neighbour = False
    path_to_rp = [] # (address:port) (Esta porta tem que ser a porta listening do node aka a porta na lista de neighbours)
    
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

        receiving_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        receiving_socket.connect((requesting_address, new_server_port))

        # 1. Check the request type
        request_type = request.split(";;")[0]

        if request_type == "CLIENT_REQUEST":
            content_name = request.split(";;")[1]
            self.client_request(requesting_address, receiving_socket, content_name)

        # A logica aqui nao esta bem, isto nao funciona em casos de maior profundidade
        elif request_type == "LOCATE_RP":
            connected_neighbour = self.locate_rp(requesting_address, receiving_socket)
            receiving_socket.send(connected_neighbour.encode())

        elif request_type == "REDIRECT_STREAM":
            self.redirect_stream(requesting_address, receiving_socket, request)

        elif request_type == "REQUEST_STREAM":
            self.request_stream(requesting_address, receiving_socket, request)

        else:
            print(f"Invalid request: {request}")
        



    def client_request(self, requesting_address, socket, content_name):
        print(f"Requesting content from {requesting_address}")

        # 1. Check if the node is currently streaming the content
        if content_name in self.streaming_content:
            print("Node has the content")
            self.redirect_current_streaming_content(requesting_address, socket, content_name)

        # 2. If not, check if we are connected to the RP
        elif self.rp_neighbour:
            print("Node is connected to the RP")
            # 2.1. If so, send the request to the RP
            self.send_request_to_rp(content_name, socket)

        # 3. If not, locate the RP
        else:
            print("Node is not connected to the RP")
            # 3.1. Send a request to the neighbours to locate the RP
            connected_neighbour = self.locate_rp(requesting_address, socket)
            # 3.2. Request the content from the RP through the connected neighbour
            self.send_request_to_rp(content_name, socket, connected_neighbour) 


    def redirect_current_streaming_content(self, requesting_address, content_name):
        receiving_socket = self.streaming_content[content_name]
        while True:
            data = receiving_socket.recv(2048)
            if not data:
                break
            requesting_address.sendall(data)


    # Vai construir um caminho de ips até ao RP
    # Quando receber uma resposta vai dar append do seu ip ao caminho e reencaminhar a resposta para o node anterior
    def locate_rp(self, requesting_address, socket):
        print(f"Locating RP from {requesting_address}")
        # 1. Send a request to the neighbours to locate the RP
        for neighbour in self.neighbours:
            # 1.1. Create a new socket to send the request
            neighbour_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            neighbour_socket.connect(neighbour)
            # 1.2. Send the request
            neighbour_socket.send("LOCATE_RP".encode())
            # 1.3. Close the socket
            neighbour_socket.close()

        
        # 2. Receive Confirmation from one of the neighbours that they are connected to the RP
        # 2.1. Receive the first neighbour address who responded 
        socket.accept()
        neighbour_address = socket.recv(1024).decode()

        return neighbour_address

            
    def send_request_to_rp(self, content_name, socket, connected_neighbour_ip):
        
        # 1. Create a new socket to send the request
        rp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if connected_neighbour_ip:
            rp_socket.connect(connected_neighbour_ip)
        else:
            rp_socket.connect(self.ip_rp)
        # 2. Send the request
        rp_socket.send(f"CONTENT_REQUEST-{content_name}".encode())
        # 3. Close the socket
        rp_socket.close()


    # Vai encaminhar os pacotes recebidos para o node seguinte no caminho recebido no pacote, acrescentando 1 ao contador de hops
    def redirect_stream(self, requesting_address, socket, request):
        pass

    # Vai encaminhar o pedido para o node seguinte no caminho para o RP acrescentando 1 ao contador de hops
    # O ultimo nodo sera responsavel por enviar o pedido ao RP
    def request_stream(self, requesting_address, socket, request):
        pass

if __name__ == "__main__":
    (Node()).main()
