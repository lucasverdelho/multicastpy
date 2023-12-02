
import sys
import socket
import threading

from Node import Node


class initNodes:
    def main(self, master):
        node1 = Node(node_id=1, port=5000)
        node2 = Node(node_id=2, port=5001)
        node3 = Node(node_id=3, port=5002)
        node4 = Node(node_id=4, port=5003)

        #Connect nodes
        node1.connect_to_node(other_node_id=2, other_node_port=5001)
        node1.connect_to_node(other_node_id=3, other_node_port=5002)

        node2.connect_to_node(other_node_id=3, other_node_port=5002)

        node4.connect_to_node(other_node_id=1, other_node_port=5000)
        node4.connect_to_node(other_node_id=2, other_node_port=5001)
        node4.connect_to_node(other_node_id=3, other_node_port=5002)

        # Send messages between nodes
        node1.send_message(dest_node_ids=[2, 3], message="Hello from Node 1 to Node 2 and 3!")

        # Allow time for messages to propagate in the network
        time.sleep(2)

        node2.send_message(dest_node_ids=[1, 2, 3], message="Hello from Node 2 to Node 1, 2, and 3!")

        # Allow time for messages to propagate in the network
        time.sleep(2)

        node4.send_message(dest_node_ids=[1, 2, 3], message="Hello from Node 4 to Node 1, 2, and 3!")



        # Allow time for messages to propagate in the network
        time.sleep(5)

        # Stop nodes
        node1.stop()
        node2.stop()
        node3.stop()
        node4.stop()



if __name__ == "__main__":
    (Node()).main()