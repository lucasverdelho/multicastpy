import threading
import socket
import sys

class NodeRP:

    neighbours = []
    serverIPs = []
    content = {}

    def main(self):
        print("Starting RP Node")
        try:
            NODE_PORT = int(sys.argv[1])
            NODE_NUMBER = int(sys.argv[2])
        except (IndexError, ValueError):
            print("[Usage: Node.py node_port node_number]\n")

        self.read_ips_from_file()
        self.read_servers_from_file()

        # 1. Create a permanent listening loop for the RTSP socket
        nodeServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        nodeServerSocket.bind(('', NODE_PORT))
        nodeServerSocket.listen(5)

        # Primeiro comunicar com os servidores e estabelecer os conteudos que cada um tem
        for server in self.serverIPs:
            # Create a new socket for each server connection
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                # Connect to the server
                server_socket.connect((server, 6000))

                # Send a request to the server
                request_msg = "CONTENT_INFO_REQUEST"
                server_socket.send(request_msg.encode())
                print(f"Sent CONTENT_INFO_REQUEST to the server {server}.")

                # Receive the content list from the server
                response = server_socket.recv(1024).decode()
                print(f"Received response from the server {server}: {response}")

                # Add the content to the content list
                self.content[server] = response

            except Exception as e:
                print(f"Error connecting to server {server}: {e}")

            finally:
                # Close the socket for this server connection
                server_socket.close()
                print(f"Closed socket for server {server}.")



    #     # MAIN LISTEN LOOP
    #     # Cria uma nova thread para cada requesição
    #     while True:

    #         # 2. Wait for any connection request
    #         requesting_socket, requesting_address = nodeServerSocket.accept()
    #         print(f"Requesting socket connected: {requesting_address}")

    #         request = requesting_socket.recv(1024).decode()

    #         # 3. Create new port for the new communication socket and send it back to the requesting node
    #         new_server_port = self.find_available_port()
    #         print(f"New server port: {new_server_port}")
    #         response_msg = f"{new_server_port}"
    #         requesting_socket.send(response_msg.encode())

    #         # 4. Create a new thread to handle the request
    #         threading.Thread(target=self.handle_request, args=(new_server_port, requesting_address, request)).start()

    #         # 5. Close the socket
    #         requesting_socket.close()



    def read_ips_from_file(self):
        # Reads the IPs of the neighboring nodes
        filename = "noderp.txt"
        with open(filename) as f:
            for line in f:
                # Remove leading and trailing whitespaces, including the newline character
                ip = line.strip()
                self.neighbours.append(ip)

    def read_servers_from_file(self):
        # Reads the IPs of servers
        filename = "servers.txt"
        with open(filename) as f:
            for line in f:
                # Remove leading and trailing whitespaces, including the newline character
                ip = line.strip()
                self.serverIPs.append(ip)


    # def handle_request(self, new_server_port, requesting_address, request):

    #     socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     socket.connect((requesting_address, new_server_port))

    #     # 1. Check the request type
    #     request_type = request.split(";;")[0]

    #     if request_type == "CONTENT_REQUEST":
    #         content_name = request.split(";;")[1]
    #         self.client_request(requesting_address, socket, content_name)



if __name__ == "__main__":
    NodeRP().main()