import socket
import sys

def connect_to_node(node_ip):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((node_ip, 5000))  # Assuming port 5000 for connections
        print(f"Connected to Node at {node_ip}")

        while True:
            content_request = input("Enter content request (or 'exit' to quit): ")
            if content_request.lower() == 'exit':
                break

            server_socket.sendall(content_request.encode())

            # Receive and print the content from the node
            data = server_socket.recv(1024)
            print(f"Received content: {data.decode()}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server_connect.py <node_ip>")
        sys.exit(1)

    node_ip = sys.argv[1]
    connect_to_node(node_ip)
