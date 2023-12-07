import sys
from tkinter import Tk
from Client import Client
import socket
import time


if __name__ == "__main__":
	try:
		node_ip = sys.argv[1]
		content_name = sys.argv[2]	
	except:
		print("[Usage: ClientLauncher.py serverIp content_name]\n")	
	

	print(f"Connecting to {node_ip}:{5000} to request content: {content_name}")
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect((node_ip, 5000))

	request_msg = f"CONTENT_REQUEST;;{content_name}"
	client_socket.send(request_msg.encode())
	print(f"Sent CONTENT_REQUEST to the RPNode at {node_ip}:{5000} for content: {content_name}")

	new_port = int(client_socket.recv(1024).decode())
	client_socket.close()

	time.sleep(2)
	print("Cnnectiong to the new port " + str(new_port))
	node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	node_socket.connect((node_ip, new_port))

	root = Tk()
	print("Created root.")
	# Create a new client
	app = Client(root, node_socket)

	print("Created client.")
	app.master.title("RTPClient")	
	
	print("Set title.")
	root.mainloop()


	


