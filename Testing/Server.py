import sys
import socket
from ServerWorker import ServerWorker
import threading
import os

# TODO
# 1. Create a permanent listening loop for the RTSP socket
# 2. Wait for a client to connect
# 3. Send the new server port and new rtp port to the client,
#    creating a new RTSP session for each client generating 
#    a new port for the RTP session
# 4. Create a new thread to handle the client, 
# 5. Close the client socket
# 6. Repeat the loop to wait for new clients

folder_path = "content/"

class Server:

    content_list = [] # List of content available in the server (video names)

    def main(self):
        print("Servidor de streaming de video iniciado")
        try:
            SERVER_PORT = int(sys.argv[1])
        except (IndexError, ValueError):
            print("[Usage: Server.py Server_port]\n")
            return  # Exit the program if the command line argument is missing or not a valid integer

        # 1. Read the content list from the file
        self.content_list = os.listdir(folder_path)

        print(self.content_list)

        # 2. Create a permanent listening loop for the server socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', SERVER_PORT))
        server_socket.listen(5)

        local_address = server_socket.getsockname()
        print(local_address)

        # 3. Accept Connection from the RP Node and send the content list
        rpsocket, rp_address = server_socket.accept()  # Unpack the tuple
        print(f"RP Node connected from {rp_address}.")

        rpsocket.recv(1024).decode()
        print("Received request from RP Node.")
        response_msg = f"{self.content_list}"
        rpsocket.send(response_msg.encode())
        print("Sent content list to RP Node.")
        rpsocket.close()
        print("Closed socket.")


    #     while True:

    #         # 2. Wait for a client to connect
    #         client_socket, client_address = server_socket.accept()
    #         print(f"Client connected: {client_address}")
    #         new_server_port = self.find_available_port()
    #         print(f"New server port: {new_server_port}")

    #         # Read the request from the client
    #         # Wait until there is data available to be received

    #         request = client_socket.recv(1024).decode()

    #         # 3. Send the new server port and new rtp port to the client
    #         #    creating a new RTSP session for each client generating
    #         #    a new port for the RTP session
    #         response_msg = f"{new_server_port}"
    #         client_socket.send(response_msg.encode())

    #         # 4. Create a new thread to handle the client
    #         threading.Thread(target=self.handle_client, args=(new_server_port, client_socket, client_address)).start()

    #         # 5. Close the client socket
    #         client_socket.close()


    # def find_available_port(self):
    #     try:
    #         temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         temp_socket.bind(('localhost', 0))  # Bind to an available port on localhost
    #         temp_socket.listen(1)
    #         port = temp_socket.getsockname()[1]
    #         temp_socket.close()
    #         return port
    #     except socket.error:
    #         print("Error finding available port.")
    #         return None



    # def handle_client(self, new_server_port, client_socket, client_address):
    #     try:
    #         # Pass the client socket and new server port to the ServerWorker
    #         server_worker_instance = ServerWorker(new_server_port)
    #         server_worker_instance.run()

    #     except Exception as e:
    #         print(f"Error handling client on new port: {e}")
    #     finally:
    #         client_socket.close()


if __name__ == "__main__":
    (Server()).main()
