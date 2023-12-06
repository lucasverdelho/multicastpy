import socket
import sys
import time

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: connect_to_testNode.py node_ip")
        sys.exit(1)

    node_ip = sys.argv[1]

    content_name = "movie.Mjpeg"
    # Create a socket to connect to the RPNode
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the RPNode
    client_socket.connect((node_ip, 5000))

    # Send a CONTENT_REQUEST
    request_msg = f"CONTENT_REQUEST;;{content_name}"
    client_socket.send(request_msg.encode())
    print(f"Sent CONTENT_REQUEST to the RPNode at {node_ip}:{5000} for content: {content_name}")

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


    print("Connected to server.")

    # Start the loop to receive RTP packets from the server and send them to the multicast group
    while True:
        data, addr = new_socket.recvfrom(20480)
        print("Received data from server.")
