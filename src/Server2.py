import sys
import socket
import threading
import random

from ServerWorker import ServerWorker

class Server:
    def main(self):
        print("Video streaming server started.")
        try:
            SERVER_PORT = int(sys.argv[1])
        except (IndexError, ValueError):
            print("[Usage: Server.py Server_port]\n")
            return

        rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rtspSocket.bind(('', SERVER_PORT))
        rtspSocket.listen(5)

        local_address = rtspSocket.getsockname()
        print(local_address)

        while True:
            client_socket, client_address = rtspSocket.accept()
            new_server_port = self.find_available_port()

            threading.Thread(target=self.handle_client, args=(new_server_port, client_socket)).start()

    def handle_client(self, new_server_port, client_socket):
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

    def find_available_port(self):
        port = random.randint(5001, 10000)
        while self.is_port_in_use(port):
            port = random.randint(5001, 10000)
        return port

    def is_port_in_use(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', port)) == 0

if __name__ == "__main__":
    Server().main()