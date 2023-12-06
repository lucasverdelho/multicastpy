import socket
import struct
# import cv2
# import numpy as np

def main():
    # Replace this value with the actual multicast group address and port in the format '224.1.1.1-5001'
    multicast_group_address = '224.1.1.1-5001'

    # Extract multicast group address and port from the combined string
    multicast_group = multicast_group_address.split('-')[0]
    multicast_port = int(multicast_group_address.split('-')[1])

    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Bind to any available port
    client_socket.bind(('', multicast_port))

    # Join the multicast group
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    client_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"Client joined multicast group: {multicast_group}:{multicast_port}")

    # OpenCV window for displaying video
    # cv2.namedWindow("Video Stream", cv2.WINDOW_NORMAL)

    # Buffer for accumulating data until a complete JPEG frame is received
    data_buffer = b''

    try:
        while True:
            data, address = client_socket.recvfrom(20480)

            # Print information about received data
            print(f"Received data from {address}")
            print(f"Data length: {len(data)}")
            print(f"Data: {data}")

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

    except Exception as main_error:
        print(f"Error in main loop: {main_error}")

    finally:
        # Release OpenCV window and close the socket
        # cv2.destroyAllWindows()
        client_socket.close()

if __name__ == "__main__":
    main()
