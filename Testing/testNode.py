import socket
import sys

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
        response = client_socket.recv(1024).decode()
        print(f"Received response from the RPNode: {response}")

    except Exception as e:
        print(f"Error connecting to the RPNode: {e}")

    finally:
        # Close the socket
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: test_node.py rp_node_ip rp_node_port content_name")
        sys.exit(1)

    rp_node_ip = sys.argv[1]
    rp_node_port = int(sys.argv[2])
    content_name = sys.argv[3]

    send_content_request(rp_node_ip, rp_node_port, content_name)