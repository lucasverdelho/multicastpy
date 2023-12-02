import sys
import threading
import socket

class Node:

    vizinhos = {} #(id, address:port)
    ip_rp = "0.0.0.0:5000"
    streaming_content = {} # (content_name, receiving_socket)

    
    def main(self):
        print("Starting Node...")
        try:
            NODE_PORT = int(sys.argv[1])
            NODE_NUMBER = int(sys.argv[2])
        except (IndexError, ValueError):
            print("[Usage: Node.py node_port node_number]\n")

        self.vizinhos = self.read_ips_from_file(NODE_NUMBER)
        
        threading.Thread(target=self.create_listening_sockets).start()

        
    def create_listening_sockets(self):
        #creates the sockets that will listen to the other nodes
        for i in range(len(self.vizinhos)):
            nodeServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            nodeServerSocket.bind(('', 6000 + i))
            nodeServerSocket.listen(5)
            threading.Thread(target=self.handle_node_communication, args=(nodeServerSocket,)).start()
    

    def handle_node_communication(self, nodeServerSocket):
        #handles the communication between nodes
        while True:
            request_socket, request_address = nodeServerSocket.accept()
            print(f"Request connected: {request_address}")
            self.handle_request(request_address, request_socket)
            request_socket.close()
            

    def read_ips_from_file(self, NODE_NUMBER):
        #reads the ips of the neighnouring nodes
        filename = "node" + NODE_NUMBER + ".txt"
        with open(filename) as f:
            for line in f: #each line will be the ip of the neighnours
                self.neighbours.append()




if __name__ == "__main__":
    (Node()).main()
