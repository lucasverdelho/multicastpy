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
        # TEMPORARILY HARDCODED!!!!!!!!!!!!!!!!!!  TODO CHANGE THIS
        nodeServerSocket.bind(('10.0.5.1', NODE_PORT)) 
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
            # TEMPORARILY HARDCODED!!!!!!!!!!!!!!!!!!  TODO CHANGE THIS
            temp_socket.bind(('10.0.5.1', 0))  # Bind to an available port on localhost
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
        # TODO METER BIND APENAS PARA A INTERFACE NECESSARIA, VER DE ONDE VEIO O PEDIDO E FAZER BIND PARA ESSA INTERFACE
        # TODO POR ENQUANTO ESTA HARDCODED, TEMOS QUE MUDAR ISTO
        handling_socket.bind(('10.0.5.1', new_server_port))
        handling_socket.listen(1)

        print(handling_socket.getsockname())
        # Accept the new connection from the node
        request_socket, server_address = handling_socket.accept()
        print(f"Accepted connection from the node: {server_address}")

        message = "ACKNOWLEDGED CONNECTION"
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
            response_msg = f"MULTICAST_STREAM;;{content_name}"
            request_socket.send(response_msg.encode())
            print(f"Sent MULTICAST_STREAM to the requesting node {requesting_address} for content: {content_name}")
        
        else:
            self.handle_multicast(content_name, request_socket) # Eventualmente temos que passar a request_socket para esta funcao responder ao pedinte


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
        multicast_group = self.generate_multicast_group()
        multicast_group_address = f"{multicast_group}-{5000 + len(self.streaming_content) + 1}"
        self.streaming_content[content_name] = multicast_group_address

        # Set up the multicast socket
        multicast_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, 
                                         proto=socket.IPPROTO_UDP, fileno=None)
        # This defines how many hops a multicast datagram can travel. 
        # The IP_MULTICAST_TTL's default value is 1 unless we set it otherwise. 
        multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 5)

        # This defines to which network interface (NIC) is responsible for
        # transmitting the multicast datagram; otherwise, the socket 
        # uses the default interface (ifindex = 1 if loopback is 0)
        # If we wish to transmit the datagram to multiple NICs, we
        # ought to create a socket for each NIC. 
        multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton('10.0.5.1'))

        print(f"Multicast group created for content: {content_name}")
        print(f"Multicast group address: {multicast_group_address}")
        print(f"Listening on: {multicast_socket.getsockname()}")

        multicast_group = self.streaming_content[content_name].split('-')[0]  # Extract multicast group address
        multicast_port = self.streaming_content[content_name].split('-')[1]  # Extract port
        print("Streaming into multicast group: " + multicast_group + ":" + multicast_port)


        # Send the Multicast IP and Port to the requesting node
        response_msg = f"MULTICAST_STREAM;;{multicast_group};;{multicast_port}"

        # Send the response to the requesting node
        request_socket.send(response_msg.encode())
        print(f"Sent MULTICAST_STREAM address to the requesting node for content: {content_name}")

        # Close the requesting socket
        request_socket.close()

        # Start the loop to receive RTP packets from the server and send them to the multicast group
        while True:
            data, addr = rtsp_socket.recvfrom(20480)
            if data:
                multicast_socket.sendto(data, (multicast_group, int(multicast_port)))
                # multicast_socket.sendto(message.encode(), (multicast_group, int(multicast_port)))
                rtp_packet = RtpPacket()
                rtp_packet.decode(data)

                curr_frame_nbr = rtp_packet.seqNum()
                print("Current Seq Num: " + str(curr_frame_nbr))

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



