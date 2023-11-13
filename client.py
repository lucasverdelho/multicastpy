import socket
import sys

def send_content_request(node_ip):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((node_ip, 5000))  # Assuming port 5000 for connections
        print(f"Connected to Node at {node_ip}")

        while True:
            content_request = input("Enter content request (or 'exit' to quit): ")
            if content_request.lower() == 'exit':
                break

            client_socket.sendall(content_request.encode())

            # Receive and print the content from the node
            data = client_socket.recv(1024)
            print(f"Received content: {data.decode()}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python client.py <node_ip>")
        sys.exit(1)

    node_ip = sys.argv[1]
    send_content_request(node_ip)
