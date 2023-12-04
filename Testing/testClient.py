import socket
import struct
import sys

def main():
    # Replace this value with the actual multicast group address and port in the format '224.1.1.1-1'
    multicast_group_address = '224.1.1.1-5001'

    # Extract multicast group address and port from the combined string
    multicast_group = multicast_group_address.split('-')[0]
    multicast_port = int(multicast_group_address.split('-')[1])

    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Bind to any available port
    client_socket.bind(('', multicast_port))

    # Join the multicast group
    # Tell the operating system to add the socket to the multicast group
    # on all interfaces.
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    client_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"Client joined multicast group: {multicast_group}:{multicast_port}")

    # Receive/respond loop
    while True:
    
        data, address = client_socket.recvfrom(20480)
        print(f"Received data from {address}")
        print(data)



if __name__ == "__main__":
    main()
