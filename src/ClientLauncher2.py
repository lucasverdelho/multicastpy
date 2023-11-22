import sys
from tkinter import Tk
from Client import Client
import socket

def request_connection(server_addr, server_port):
    try:
        # Create a socket to connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_addr, int(server_port)))

        # Send a request to the server
        request_msg = "CONNECT_REQUEST"
        client_socket.send(request_msg.encode())
        print("Sent CONNECT_REQUEST to the server.")

        # Wait until there is data available to be received
        while not client_socket.recv(1024):
            pass

        # Receive the new ports from the server
        response = client_socket.recv(1024).decode()
        print(f"Received response from the server: {response}")
        
        # Split the response into server port and rtp port
        new_server_port, new_rtp_port = map(int, response.split(','))

        # Close the socket
        client_socket.close()

        return new_server_port, new_rtp_port

    except Exception as e:
        print(f"Error requesting connection: {e}")
        return None, None

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("[Usage: ClientLauncher.py Server_name Server_port Video_file]\n")
        sys.exit(1)

    try:
        serverAddr = sys.argv[1]
        serverPort = sys.argv[2]

        print(f"Connecting to server: {serverAddr}:{serverPort}")

        # Request connection to get new serverPort and rtpPort
        new_server_port, new_rtp_port = request_connection(serverAddr, serverPort)

        if new_server_port is None or new_rtp_port is None:
            print("Failed to establish connection with the server.")
            sys.exit(1)

        print(f"Received new ports from the server: serverPort={new_server_port}, rtpPort={new_rtp_port}")

        # Use the new ports for communication
        serverPort = new_server_port
        rtpPort = new_rtp_port
        fileName = sys.argv[3]
    except Exception as e:
        print("[Usage: ClientLauncher.py Server_name Server_port Video_file]\n")
        sys.exit(1)

    root = Tk()

    # Create a new client with the updated ports
    app = Client(root, serverAddr, serverPort, rtpPort, fileName)
    app.master.title("RTPClient")
    root.mainloop()