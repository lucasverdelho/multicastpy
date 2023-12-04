import socket
import struct

def main():
    # Replace this value with the actual multicast group address and port in the format '224.1.1.1-1'
    multicast_group_address = '224.1.1.1-0'

    # Extract multicast group address and port from the combined string
    multicast_group = multicast_group_address.split('-')[0]
    multicast_port = int(multicast_group_address.split('-')[1])

    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Set the time-to-live for the multicast packets
    client_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack('b', 1))

    # Bind to any available port
    client_socket.bind(('0.0.0.0', 0))

    # Join the multicast group
    client_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(multicast_group) + socket.inet_aton('0.0.0.0'))

    print(f"Client joined multicast group: {multicast_group}:{multicast_port}")

    try:
        while True:
            data, addr = client_socket.recvfrom(20480)
            # Process the received data (e.g., display or save frames)
            print("Received data from {}: {}".format(addr, len(data)))
    except KeyboardInterrupt:
        print("Client interrupted.")

    finally:
        # Leave the multicast group
        client_socket.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, socket.inet_aton(multicast_group) + socket.inet_aton('0.0.0.0'))
        client_socket.close()
        print("Client left multicast group.")

if __name__ == "__main__":
    main()
