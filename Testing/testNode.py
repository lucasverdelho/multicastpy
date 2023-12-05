import socket
import sys
import time
# import cv2
# import numpy as np
import struct

streaming_content = {} # Dicionario com o nome do conteudo e o socket que esta a fazer streaming

def send_content_request(node_ip, node_port, content_name, requesting_socket):
    # Create a socket to connect to the RPNode
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the RPNode
    client_socket.connect((node_ip, node_port))

    # Send a CONTENT_REQUEST
    request_msg = f"CONTENT_REQUEST;;{content_name}"
    client_socket.send(request_msg.encode())
    print(f"Sent CONTENT_REQUEST to the RPNode at {node_ip}:{node_port} for content: {content_name}")

    # Receive the response from the RPNode
    new_port = client_socket.recv(1024).decode()
    print(f"Received response from the RPNode: {new_port}")

    # Close the initial socket
    client_socket.close()

    time.sleep(2)

    # Connect to the new port
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("connecting to the new port " + new_port)
    new_socket.connect((node_ip, int(new_port)))
    time.sleep(1)
    print("connecting to the new port " + new_port)

    multicast_group_address = ''
    multicast_group_port = 0
    print("waiting for response")

    while True:
        response_bytes = new_socket.recv(1024)
        response = response_bytes.decode()

        if response.startswith("MULTICAST_STREAM"):
            multicast_group_address = response.split(';;')[1]
            multicast_group_port = response.split(';;')[2]
            print(f"Received MULTICAST_STREAM from the RPNode at {node_ip}:{new_port} for content: {content_name}")
            print(f"Multicast group address: {multicast_group_address}")
            print(f"Multicast group port: {multicast_group_port}")
            get_multicast_stream(multicast_group_address, int(multicast_group_port),requesting_socket)
            break

        print(f"Received data from the RPNode at {node_ip}:{new_port}")
        print(response)
        time.sleep(1)

    print("Exited the loop")  # Add this line to check if the loop is exited
    new_socket.close()  # Close the new_socket after exiting the loop



        

def get_multicast_stream(multicast_group_address, multicast_group_port, requesting_socket):

    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Bind to any available port
    client_socket.bind(('', multicast_group_port))

    # Join the multicast group
    group = socket.inet_aton(multicast_group_address)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    client_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"Client joined multicast group: {multicast_group_address}:{multicast_group_port}")

    try:
        while True:
            data, address = client_socket.recvfrom(20480)

            # Print information about received data
            print(f"Received data from {address}")
            print(f"Data length: {len(data)}")
            print(f"Data: {data}")

            # Send the data to the requesting socket
            requesting_socket.send(data)

    except Exception as main_error:
        print(f"Error in main loop: {main_error}")

    finally:
        client_socket.close()






if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: test_node.py rp_node_ip rp_node_port content_name")
        sys.exit(1)

    rp_node_ip = sys.argv[1]
    rp_node_port = int(sys.argv[2])
    content_name = sys.argv[3]

    # Create a socket to accept the incoming connection from the client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 7770))  # Bind to any available port
    server_socket.listen(1)

    print("Waiting for a connection from the client...")
    requesting_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    send_content_request(rp_node_ip, rp_node_port, content_name, requesting_socket)
