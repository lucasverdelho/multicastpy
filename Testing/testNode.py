import socket
import sys
import time

def send_content_request(node_ip, node_port, content_name):
    # Create a socket to connect to the RPNode
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
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
        print(f"Connected to the new port {new_port}")

        # Now you can continue communication on the new socket
        while True:
            response  = new_socket.recv(1024)
            print(f"Received data from the RPNode at {node_ip}:{new_port}")
            print(response)
            time.sleep(1)

    except Exception as e:
        print(f"Error connecting to the RPNode: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: test_node.py rp_node_ip rp_node_port content_name")
        sys.exit(1)

    rp_node_ip = sys.argv[1]
    rp_node_port = int(sys.argv[2])
    content_name = sys.argv[3]

    send_content_request(rp_node_ip, rp_node_port, content_name)
