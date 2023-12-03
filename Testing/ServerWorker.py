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

    def run(self):
        # Create new socket, bind to server port, and accept client connection
        rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rtspSocket.bind(('', self.serverPort))
        rtspSocket.listen(5)
        print("Listening for connections...")
        clientInfo = {}
        clientInfo['rtspSocket'] = rtspSocket.accept()
        print("Client connected.")
        self.clientInfo = clientInfo
        self.sendRtp()

    def sendRtp(self):
        """Send RTP packets over UDP."""
        while True:
            data = self.clientInfo['videoStream'].nextFrame()
            if data:
                frameNumber = self.clientInfo['videoStream'].frameNbr()
                try:
                    # Get the client address and port for UDP communication
                    client_address = self.clientInfo['rtspSocket'][1]
                    address = client_address[0]
                    port = int(client_address[1])
                    self.clientInfo['rtspSocket'][0].sendto(self.makeRtp(data, frameNumber), (address, port))
                except:
                    print("Connection Error")
                    traceback.print_exc(file=sys.stdout)

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


