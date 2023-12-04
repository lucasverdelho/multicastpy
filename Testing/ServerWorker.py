import sys, traceback, threading, socket
from VideoStream import VideoStream
from RtpPacket import RtpPacket
import time

class ServerWorker:

    serverPort = 0

    def __init__(self, serverPort):
        self.serverPort = serverPort
        print("Created server worker.")
        print(f"Server port: {self.serverPort}")

    def receive_request(self):
        # Create a new socket for listening
        rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        rtspSocket.bind(('127.0.0.1', self.serverPort))
        rtspSocket.listen(5)

        print("Listening for connections...")

        try:
            # Accept a connection from the client
            clientSocket, clientAddr = rtspSocket.accept()
            print(f"Client connected: {clientAddr}")

            # Receive the request from the client
            content_name = clientSocket.recv(1024).decode()
            print(f"Received request from client: {content_name}")

            # Handle the received request (you can replace this with your logic)
            self.sendRtp(content_name, clientSocket)

            # Optionally, you can send a response back to the client
            response = "OK"
            clientSocket.send(response.encode())
            
        except Exception as e:
            print(f"Error accepting client connection: {e}")
        finally:
            # Close the client socket
            if 'clientSocket' in locals():
                clientSocket.close()

            # Close the server socket
            rtspSocket.close()

        print("Server socket closed.")

    def sendRtp(self, content_name, clientSocket):
        video_stream = VideoStream(content_name)
        frame_number = 0

        while True:
            frame = video_stream.nextFrame()
            if not frame:
                # End of video stream
                break

            try:
                # Create an RTP packet
                rtp_packet = self.makeRtp(frame, frame_number)

                # Convert the RTP packet to bytes before sending
                rtp_bytes = bytes(rtp_packet)

                # Send the RTP packet over the existing client socket
                clientSocket.send(rtp_packet)

                # Wait for a short time to simulate real-time streaming
                # time.sleep(0.05)

                frame_number += 1
            except Exception as e:
                print(f"Error sending RTP packet: {e}")


    def makeRtp(self, payload, frameNbr):
        """RTP-packetize the video data."""
        version = 2
        padding = 0
        extension = 0
        cc = 0
        marker = 0
        pt = 26  # MJPEG type
        seqnum = frameNbr
        ssrc = 0

        rtpPacket = RtpPacket()

        rtpPacket.encode(version, padding, extension, cc, seqnum, marker, pt, ssrc, payload)

        return rtpPacket.getPacket()


