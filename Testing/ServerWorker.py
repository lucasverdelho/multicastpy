import sys, traceback, threading, socket
from VideoStream import VideoStream
from RtpPacket import RtpPacket

class ServerWorker:
    PLAYING = 2
    state = PLAYING

    serverPort = 0
    clientInfo = {}

    def __init__(self, serverPort):
        self.serverPort = serverPort
        print("Created server worker.")
        print(f"Server port: {self.serverPort}")

    def receive_request(self):
        rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rtspSocket.bind(('127.0.0.1', self.serverPort))
        print(f"Server socket: {rtspSocket.getsockname()}")
        rtspSocket.listen(5)
        print("Listening for connections...")

        try:
            clientSocket, clientAddr = rtspSocket.accept()
            print("Client connected.")
            self.clientInfo['rtspSocket'] = (clientSocket, clientAddr)
            self.sendRtp()
        except Exception as e:
            print(f"Error accepting client connection: {e}")
        finally:
            rtspSocket.close()

    def sendRtp(self):
            while self.state == self.PLAYING:  # Add a condition to break out of the loop
                data = self.clientInfo['videoStream'].nextFrame()
                if data:
                    frameNumber = self.clientInfo['videoStream'].frameNbr()
                    try:
                        client_address = self.clientInfo['rtspSocket'][1]
                        address = client_address[0]
                        port = int(client_address[1])
                        self.clientInfo['rtspSocket'][0].sendto(self.makeRtp(data, frameNumber), (address, port))
                    except:
                        print("Connection Error")
                        traceback.print_exc(file=sys.stdout)
                        break  # Break out of the loop in case of an error


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


