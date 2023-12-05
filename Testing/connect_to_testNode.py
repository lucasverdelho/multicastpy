import socket
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: connect_to_testNode.py server_ip server_port")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    rtsp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rtsp_socket.connect((server_ip, server_port))

    print("Connected to server.")
    
    # Start the loop to receive RTP packets from the server and send them to the multicast group
    while True:
        data, addr = rtsp_socket.recvfrom(20480)
        print(data)
