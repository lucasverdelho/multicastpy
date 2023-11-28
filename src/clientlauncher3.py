import sys
from tkinter import Tk
from Client import Client
import socket


# TODO
# 1. Send connect request to server
# 2. Receive response from server: new server port and new rtp port
# 3. Close the socket
# 4. Call Client.py with the new server port and new rtp port


if __name__ == "__main__":
	try:
		serverAddr = sys.argv[1]
		serverPort = sys.argv[2]
		fileName = sys.argv[3]	
	except:
		print("[Usage: ClientLauncher.py Server_name Server_port RTP_port Video_file]\n")	
	

	try:
		print(f"Connecting to server: {serverAddr}:{serverPort}")

		# Create a socket to connect to the server
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print("Created socket.")

		# After creating the socket
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Connect to the server
		client_socket.connect((serverAddr, int(serverPort)))

		# Send a request to the server
		request_msg = "CONNECT_REQUEST"
		client_socket.send(request_msg.encode())
		print("Sent CONNECT_REQUEST to the server.")

		# Receive the new port from the server
		response = client_socket.recv(1024).decode()
		print(f"Received response from the server: {response}")

		# Split the response into server port and rtp port
		new_server_port = int(response)

		# Close the socket
		client_socket.close()

		root = Tk()
	
		# Create a new client
		app = Client(root, serverAddr, new_server_port, new_server_port, fileName)
		app.master.title("RTPClient")	
		root.mainloop()

	except:
		print("Failed to establish connection with the server.")
		sys.exit(1)



	


