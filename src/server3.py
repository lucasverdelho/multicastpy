import sys
import socket
from ServerWorker import ServerWorker
import threading

# TODO
# 1. Create a permanent listening loop for the RTSP socket
# 2. Wait for a client to connect
# 3. Send the new server port and new rtp port to the client,
#    creating a new RTSP session for each client generating 
#    a new port for the RTP session
# 4. Create a new thread to handle the client, 
# 5. Close the client socket
# 6. Repeat the loop to wait for new clients


class Server:
    def main(self):
        print("Servidor de streaming de video iniciado")
        try:
            SERVER_PORT = int(sys.argv[1])
        except (IndexError, ValueError):
            print("[Usage: Server.py Server_port]\n")
            return  # Exit the program if the command line argument is missing or not a valid integer


        # 1. Create a permanent listening loop for the RTSP socket
        rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rtspSocket.bind(('', SERVER_PORT))
        rtspSocket.listen(5)

        local_address = rtspSocket.getsockname()
        print(local_address)

        while True:

            # 2. Wait for a client to connect
            print("Waiting for a client to connect...")
            client_socket, client_address = rtspSocket.accept()
            print(f"Client connected: {client_address}")
            new_server_port = self.find_available_port()
            print(f"New server port: {new_server_port}")

            # Read the request from the client
            # Wait until there is data available to be received

            request = client_socket.recv(1024).decode()
            print(f"Received request from the client: {request}")

            # 3. Send the new server port and new rtp port to the client
            #    creating a new RTSP session for each client generating
            #    a new port for the RTP session
            response_msg = f"{new_server_port}"
            print(f"Sending response to the client: {response_msg}")
            client_socket.send(response_msg.encode())
            print("Response sent to the client.")



            # threading.Thread(target=self.handle_client, args=(new_server_port, client_socket, client_address)).start()

            client_socket.close()


    def find_available_port(self):
        # This function can be used to find an available port for the RTP session
        # You can modify this based on your requirements
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



    def handle_client(self, new_server_port, client_socket, client_address):
        try:
            # Send the new server port to the client
            response_msg = f"{new_server_port}"
            print(f"Sending response to the client: {response_msg}")
            client_socket.send(response_msg.encode())

            # Pass the client socket and new server port to the ServerWorker
            server_worker_instance = ServerWorker({'rtspSocket': (client_socket, client_address), 'serverPort': new_server_port})
            server_worker_instance.run()

        except Exception as e:
            print(f"Error handling client on new port: {e}")
        finally:
            client_socket.close()


if __name__ == "__main__":
    (Server()).main()
