import socket
from RtpPacket import RtpPacket  # Import the appropriate module/class for RTP packet decoding

class ClientReceiver:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = None

    def setup_connection(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.bind(('localhost', 0))  # Bind to a random available local port
        print(f"Client connected. Local address: {self.client_socket.getsockname()}")

    def receive_rtp_packets(self):
        while True:
            data, addr = self.client_socket.recvfrom(2048)  # Adjust buffer size accordingly
            rtp_packet = RtpPacket()
            rtp_packet.decode(data)

            # Process the received RTP packet as needed
            payload = rtp_packet.getPayload()
            frame_number = rtp_packet.getSeqNum()

            print(f"Received RTP packet. Frame Number: {frame_number}, Payload Length: {len(payload)}")

    def close_connection(self):
        if self.client_socket:
            self.client_socket.close()
            print("Client socket closed.")

# Example Usage
# server_address = '127.0.0.1'  # Set your server address
# server_port = 1234  # Set your server port
# client_receiver = ClientReceiver(server_address, server_port)
# client_receiver.setup_connection()
# client_receiver.receive_rtp_packets()  # This will block and continuously receive RTP packets
# # You may need to interrupt the program to stop receiving packets
# client_receiver.close_connection()
