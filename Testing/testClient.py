import socket
import struct
# import cv2
# import numpy as np
import time
import sys

def main():

    if len(sys.argv) != 3:
        print("Usage: testClient.py node_ip content_name")
        sys.exit(1)

    node_ip = sys.argv[1]
    content_name = sys.argv[2]
    # Create a socket to connect to the RPNode
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the RPNode
    client_socket.connect((node_ip, 5000))

    # Send a CONTENT_REQUEST
    request_msg = f"CONTENT_REQUEST;;{content_name}"
    client_socket.send(request_msg.encode())
    print(f"Sent CONTENT_REQUEST to the RPNode at {node_ip}:{5000} for content: {content_name}")

    # Receive the response from the RPNode
    new_port = client_socket.recv(1024).decode()
    print(f"Received response from the RPNode: {new_port}")

    # Close the initial socket
    client_socket.close()

    time.sleep(2)

    # Connect to the new port
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("connecting to the new port " + new_port)
    new_socket.connect((node_ip, int(new_port)))
    time.sleep(1)
    print("connecting to the new port " + new_port)


    print("Connected to server.")

    # Start the loop to receive RTP packets from the server and send them to the multicast group
    while True:
        data, addr = new_socket.recvfrom(20480)
        # print(data)

        # Print information about received data
        print(f"Data length: {len(data)}")
        # print(f"Data: {data}")

        # # Accumulate data in the buffer
        # data_buffer += data

        # # Check for the JPEG frame boundaries
        # if b'\xff\xd8' in data_buffer and b'\xff\xd9' in data_buffer:
        #     # Find the start and end of the JPEG frame
        #     frame_start = data_buffer.find(b'\xff\xd8')
        #     frame_end = data_buffer.find(b'\xff\xd9') + 2

        #     # Extract the JPEG frame
        #     jpeg_frame = data_buffer[frame_start:frame_end]

        #     try:
        #         # Decode the JPEG frame with OpenCV
        #         frame = cv2.imdecode(np.frombuffer(jpeg_frame, dtype=np.uint8), cv2.IMREAD_COLOR)

        #         # Display the video frame
        #         cv2.imshow("Video Stream", frame)

        #         # Reset the buffer after extracting a complete frame
        #         data_buffer = data_buffer[frame_end:]
        #     except Exception as decode_error:
        #         print(f"Error decoding image: {decode_error}")

        # # Break the loop if 'q' key is pressed
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break


    # Release OpenCV window and close the socket
    # cv2.destroyAllWindows()
    client_socket.close()

if __name__ == "__main__":
    main()