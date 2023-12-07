from tkinter import *
from PIL import Image
from PIL import ImageTk
import socket
import threading
import os
from RtpPacket import RtpPacket

CACHE_FILE_NAME = "cache-"
CACHE_FILE_EXT = ".jpg"

class Client:
    INIT = 0
    READY = 1
    PLAYING = 2
    state = INIT

    def __init__(self, master, node_socket):
        self.master = master
        self.create_widgets()
        self.node_socket = node_socket
        self.frame_nbr = 0
        self.listen_rtp()

    def create_widgets(self):
        """Build GUI."""
        # Create a label to display the movie
        self.label = Label(self.master, height=19)
        self.label.grid(row=0, column=0, columnspan=4, sticky=W + E + N + S, padx=5, pady=5)

    def listen_rtp(self):
        print("INITING")
        """Listen for RTP packets."""
        while True:
            try:
                print("beans")
                data = self.node_socket.recv(20480)
                if data:
                    rtp_packet = RtpPacket()
                    rtp_packet.decode(data)

                    curr_frame_nbr = rtp_packet.seqNum()
                    print("Current Seq Num: " + str(curr_frame_nbr))

                    if curr_frame_nbr > self.frame_nbr:
                        self.frame_nbr = curr_frame_nbr
                        self.update_movie(self.write_frame(rtp_packet.getPayload()))
            except Exception as e:
                print("Error while listening for RTP packets:", str(e))
                break

    def write_frame(self, data):
        """Write the received frame to a temp image file. Return the image file."""
        cache_name = CACHE_FILE_NAME + CACHE_FILE_EXT
        file = open(cache_name, "wb")
        file.write(data)
        file.close()

        return cache_name

    def update_movie(self, image_file):
        """Update the image file as a video frame in the GUI."""
        photo = ImageTk.PhotoImage(Image.open(image_file))
        self.label.configure(image=photo, height=288)
        self.label.image = photo