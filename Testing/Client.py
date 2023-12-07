from tkinter import *
from PIL import Image
from PIL import ImageTk
import socket
import threading
from RtpPacket import RtpPacket
import time

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
		self.rtspSeq = 0
		self.sessionId = 0
		threading.Thread(target=self.listenRtp).start()

	def create_widgets(self):
		"""Build GUI."""
		# Create a label to display the movie
		self.label = Label(self.master, height=19)
		self.label.grid(row=0, column=0, columnspan=4, sticky=W + E + N + S, padx=5, pady=5)

	def listenRtp(self):
		print("INITING")
		"""Listen for RTP packets."""
		while True:
			try:
				data, addr = self.node_socket.recvfrom(20480)
				if data:
					print(f"Data length: {len(data)}")
					
					try:
						rtp_packet = RtpPacket()
						rtp_packet.decode(data)
								
						curr_frame_nbr = rtp_packet.seqNum()
						print("Current Seq Num: " + str(curr_frame_nbr))

						if curr_frame_nbr > self.frame_nbr:
							self.frame_nbr = curr_frame_nbr
							self.update_movie(self.writeFrame(rtp_packet.getPayload()))

					except:
						time.sleep(0.05)
						print("Packet not valid")
						continue

			except Exception as e:
				print("Error while listening for RTP packets:", str(e))
				break

	def writeFrame(self, data):
		"""Write the received frame to a temp image file. Return the image file."""
		cachename = CACHE_FILE_NAME + str(self.sessionId) + CACHE_FILE_EXT
		file = open(cachename, "wb")
		file.write(data)
		file.close()
		
		return cachename

	def update_movie(self, image_file):
		"""Update the image file as a video frame in the GUI."""
		photo = ImageTk.PhotoImage(Image.open(image_file))
		self.label.configure(image=photo, height=288)
		self.label.image = photo