import socket
import threading
from VideoStream import VideoStream
from RtpPacket import RtpPacket
import time

class ServerWorker:
    def __init__(self, server_port, filename):
        self.server_port = server_port
        self.filename = filename

    def run(self):
        rtsp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rtsp_socket.bind(('', self.server_port))
        rtsp_socket.listen(1)

        print("Server is listening for connections...")
        conn_socket, client_addr = rtsp_socket.accept()
        print("Client connected.")

        # Start a new thread to handle the RTP streaming
        threading.Thread(target=self.send_rtp, args=(conn_socket,)).start()

    def send_rtp(self, conn_socket):
        video_stream = VideoStream(self.filename)
        frame_number = 0

        while True:
            time.sleep(0.05)
            data = video_stream.nextFrame()
            if data:
                try:
                    # Use send instead of sendto for TCP connections
                    conn_socket.send(self.make_rtp(data, frame_number))
                    frame_number += 1
                except Exception as e:
                    print(f"Connection Error: {e}")
                    break

    def make_rtp(self, payload, frame_nbr):
        version, padding, extension, cc, marker, pt, seq_num, ssrc = 2, 0, 0, 0, 0, 26, frame_nbr, 0
        rtp_packet = RtpPacket()
        rtp_packet.encode(version, padding, extension, cc, seq_num, marker, pt, ssrc, payload)
        return rtp_packet.getPacket()

