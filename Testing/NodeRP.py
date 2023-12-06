import threading
import socket
import sys
import time
import NodeRPWorker 
from RtpPacket import RtpPacket
import struct

class NodeRP:

    neighbours = []
    serverIPs = []
    content = {}
    streaming_content = {}

    def main(self):
        print("Starting RP Node")
        try:
            NODE_PORT = int(sys.argv[1])
        except (IndexError, ValueError):
            print("[Usage: Node.py node_port]\n")

        self.read_ips_from_file()
        self.read_servers_from_file()

        # 1. Create a permanent listening loop for the RTSP socket
        nodeServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Listen on all interfaces
        nodeServerSocket.bind(('0.0.0.0', NODE_PORT)) 
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



        ## TEMORARILY ADD CONTENT TO THE CONTENT LIST MANUALLY
        # self.content["localhost:6000"] = ["movie1.Mjpg"]

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

            # Create a new thread to handle the request
            threading.Thread(target=self.handle_request, args=(new_server_port, requesting_address, request)).start()

            # Close the socket for this connection
            requesting_socket.close()



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


    def find_available_port(self):
        try:
            temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            temp_socket.bind(('0.0.0.0', 0))  # Bind to an available port on localhost
            temp_socket.listen(1)
            port = temp_socket.getsockname()[1]
            temp_socket.close()
            return port
        except socket.error:
            print("Error finding available port.")
            return None

    
    def handle_request(self, new_server_port, requesting_address, request):
        # Create a new socket for each server connection
        handling_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Listen on all interfaces
        handling_socket.bind(('0.0.0.0', new_server_port))
        handling_socket.listen(1)

        print(handling_socket.getsockname())
        # Accept the new connection from the node
        request_socket, server_address = handling_socket.accept()
        print(f"Accepted connection from the node: {server_address}")

        message = f"ACKNOWLEDGED CONNECTION"
        request_socket.send(message.encode())

        # 1. Check the request type
        request_type = request.split(";;")[0]

        if request_type == "CONTENT_REQUEST":
            content_name = request.split(";;")[1]
            self.content_request(requesting_address, request_socket, content_name)
            print(f"Sent CONTENT_REQUEST to the server for the content: {content_name}")





    def content_request(self, requesting_address, request_socket, content_name):
        # 1. Check if there already exists a multicast group for the content
        if content_name in self.streaming_content:
            # 1.1. If there is, redirect the requesting node to the multicast group
            self.redirect_to_multicast(requesting_address, request_socket, content_name)
        
        else:
            self.handle_multicast(content_name, request_socket) # Eventualmente temos que passar a request_socket para esta funcao responder ao pedinte

    def redirect_to_multicast(self, requesting_address, request_socket, content_name):
        # 1.1. If there is, redirect the requesting node to the multicast group
        time.sleep(2)
        multicast_group_address = self.streaming_content[content_name].split('-')[0]
        multicast_group_port = self.streaming_content[content_name].split('-')[1]
        response_msg = f"MULTICAST_STREAM;;{multicast_group_address};;{multicast_group_port}"
        print(response_msg)
        request_socket.send(response_msg.encode())
        print(f"Sent MULTICAST_STREAM to the requesting node {requesting_address} for content: {content_name}")


    def handle_multicast(self, content_name, request_socket):
        # We need to create a new multicast group for the content after getting a unicast stream from the server to us of the content
        # Locate which server has the content
        server = self.find_server_with_content(content_name)

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((server, 6000))

        # Send a request to the server
        request_msg = f"REQUEST_STREAM;;{content_name}"
        server_socket.send(request_msg.encode())

        # Receive the new port from the server
        response = server_socket.recv(1024).decode()
        print(f"Received response from the server: {response}")

        # Split the response into server port
        new_server_port = int(response)

        # Close the socket
        server_socket.close()

        time.sleep(2)

        rtsp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rtsp_socket.connect((server, new_server_port))

        print('\nConnecting to server on port ' + str(new_server_port) + '...')

        # Add the socket to the streaming_content dictionary with an index
        multicast_group_base = '224.1.1.1'
        multicast_port = 5000 + len(self.streaming_content) + 1
        multicast_group_address = (multicast_group_base, multicast_port)
        self.streaming_content[content_name] = multicast_group_address


        # List of NICs to create sockets for
        nic_addresses = ['10.0.7.2', '10.0.22.2', '10.0.11.2', '10.0.8.1', '10.0.5.1']

        # Set up a multicast socket for each NIC
        multicast_sockets = []
        for nic_address in nic_addresses:
            multicast_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP, fileno=None)
            
            # Set multicast TTL
            multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 5)
            
            # Set multicast NIC
            multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(nic_address))
            
            # Append the multicast socket to the list
            multicast_sockets.append(multicast_socket)

        # Send Multicast IP and Port to the requesting node for each NIC
        for multicast_socket in multicast_sockets:
            response_msg = f"MULTICAST_STREAM;;{multicast_group_base};;{multicast_port}"
            
            # Send the response to the requesting node
            request_socket.send(response_msg.encode())
            print(f"Sent MULTICAST_STREAM address to the requesting node for content: {content_name}")
            
            # Close the requesting socket
            request_socket.close()

        # Start the loop to receive RTP packets from the server and send them to the multicast group for each NIC
        while True:
            data, addr = rtsp_socket.recvfrom(20480)
            if data:
                for multicast_socket in multicast_sockets:
                    multicast_socket.sendto(data, (multicast_group_base, int(multicast_port)))
                    
                rtp_packet = RtpPacket()
                rtp_packet.decode(data)

                curr_frame_nbr = rtp_packet.seqNum()
                # Implement logic to store or display the received video frames





    def generate_multicast_group(self):
        # Generate a unique multicast group address for each stream
        multicast_group_base = '224.1.1.1'  # You can choose a different base address if needed
        return multicast_group_base

    


    def find_server_with_content(self, content_name):
        for server in self.content:
            if content_name in self.content[server]:
                return server
        return None


if __name__ == "__main__":
    NodeRP().main()



