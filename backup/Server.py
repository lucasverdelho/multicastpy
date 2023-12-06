import sys
import socket
from ServerWorker import ServerWorker
import threading
import os

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



        # MAIN LISTEN LOOP
        while True:

            # 2. Wait for a client to connect
            client_socket, client_address = server_socket.accept()
            print(f"Client connected: {client_address}")

            # Read the request from the client
            # Wait until there is data available to be received

            request = client_socket.recv(1024).decode()
            requests = request.split(";;")

            print(f"Request: {requests}")
            if requests[0] == "CONTENT_INFO_REQUEST":
                # 3. Send the content list to the RP Node
                print("RP Node connected.")
                response_msg = f"{self.content_list}"
                client_socket.send(response_msg.encode())
                print("Sent content list to RP Node.")
                client_socket.close()
                print("Closed socket.")
                continue

            elif requests[0] == "REQUEST_STREAM":
                new_server_port = self.find_available_port()
                print(f"New server port: {new_server_port}")
                # 3. Send the new server port and new rtp port to the client
                #    creating a new RTSP session for each client generating
                #    a new port for the RTP session
                response_msg = f"{new_server_port}"
                client_socket.send(response_msg.encode())
                    

                # 4. Create a new thread to handle the client
                threading.Thread(target=self.handle_client, args=(new_server_port, requests)).start()

                # 5. Close the client socket
                client_socket.close()
            else :
                print("Invalid request.")
                client_socket.close()
                continue


    def find_available_port(self):
        try:
            temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            temp_socket.bind(('localhost', 0))  # Bind to an available port on localhost
            temp_socket.listen(1)
            port = temp_socket.getsockname()[1]
            temp_socket.close()
            return port
        except socket.error:
            print("Error finding available port.")
            return None



    def handle_client(self, new_server_port,requests):

        print("Initiating server worker...")
        path_to_file = folder_path + requests[1]
        # Pass the client socket and new server port to the ServerWorker
        server_worker_instance = ServerWorker(new_server_port, path_to_file)
        server_worker_instance.run()




if __name__ == "__main__":
    (Server()).main()
