import sys
import socket
from ServerWorker import ServerWorker

class Server:
    def main(self):
        print("Servidor de streaming de video iniciado")
        try:
            SERVER_PORT = int(sys.argv[1])
        except (IndexError, ValueError):
            print("[Usage: Server.py Server_port]\n")
            return  # Exit the program if the command line argument is missing or not a valid integer

        rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rtspSocket.bind(('', SERVER_PORT))
        rtspSocket.listen(5)

        local_address = rtspSocket.getsockname()
        print(local_address)
        # Receive client info (address,port) through RTSP/TCP session
        while True:
            clientInfo = {}
            clientInfo['rtspSocket'] = rtspSocket.accept()
            ServerWorker(clientInfo).run()

if __name__ == "__main__":
    (Server()).main()
