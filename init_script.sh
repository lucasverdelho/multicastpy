#!/bin/bash

# Set the process ID
PROCESS_ID="38751"

# List of nodes for which you want to run vcmd commands
NODES=("n1" "n2" "n3" "n4" "n5" "n6" "n7" "n8" "n9" "n10" "n11" "n12" "n13" "n14" "n15" "n16" "n17" "n18" "n24" "n25" "n26") 

# Source folder for file copies
SOURCE_FOLDER="/home/core/multicastpy"

# Your custom commands
CUSTOM_COMMAND_INIT_NODE="echo 'Hello from Node (RP)'"
CUSTOM_COMMAND_INIT_CLIENT="echo 'Hello from Node (Client)'"
CUSTOM_COMMAND_INIT_SERVER="python3 Server.py 6000"

# Iterate over nodes and run vcmd commands
for NODE in "${NODES[@]}"; do
    case $NODE in
        "n1"|"n2"|"n5"|"n10"|"n25"|"n7") 
            vcmd -c "/tmp/pycore.${PROCESS_ID}/${NODE}" -- bash -c "
                cp ${SOURCE_FOLDER}/Testing/*.py .
                cp ${SOURCE_FOLDER}/Testing/neighbour_lists/* .
                "
            ;;
        "n11"|"n12"|"n13"|"n14"|"n15"|"n16"|"n18"|"n26")
            vcmd -c "/tmp/pycore.${PROCESS_ID}/${NODE}" -- bash -c "
                cp ${SOURCE_FOLDER}/Testing/Client.py .
                cp ${SOURCE_FOLDER}/Testing/RtpPacket.py .
                cp ${SOURCE_FOLDER}/Testing/VideoStream.py .
                cp ${SOURCE_FOLDER}/Testing/testClient.py .
                cp ${SOURCE_FOLDER}/Testing/connect_to_node.py .
                cp ${SOURCE_FOLDER}/Testing/test_locate_rp.py .
                "
            ;;
        "n17") # SERVER 1
            vcmd -c "/tmp/pycore.${PROCESS_ID}/${NODE}" -- bash -c "
                cp ${SOURCE_FOLDER}/Testing/Server.py .
                cp ${SOURCE_FOLDER}/Testing/ServerWorker.py .
                cp ${SOURCE_FOLDER}/Testing/VideoStream.py .
                cp ${SOURCE_FOLDER}/Testing/RtpPacket.py .
                mkdir -p content  # Create 'content' folder if it doesn't exist
                cp ${SOURCE_FOLDER}/Testing/movie.Mjpeg content/.
                "
            ;;
        "n24") # SERVER 2
            vcmd -c "/tmp/pycore.${PROCESS_ID}/${NODE}" -- bash -c "
                cp ${SOURCE_FOLDER}/Testing/Server.py .
                cp ${SOURCE_FOLDER}/Testing/ServerWorker.py .
                cp ${SOURCE_FOLDER}/Testing/VideoStream.py .
                cp ${SOURCE_FOLDER}/Testing/RtpPacket.py .
                mkdir -p content  # Create 'content' folder if it doesn't exist
                cp ${SOURCE_FOLDER}/Testing/movie2.Mjpeg content/.
                "
            ;;
    esac
done

sleep 1

# Iterate over nodes and run vcmd commands for custom initialization commands
for NODE in "${NODES[@]}"; do
    case $NODE in
        "n7")
            vcmd -c "/tmp/pycore.${PROCESS_ID}/${NODE}" -- bash -c "
                $CUSTOM_COMMAND_INIT_NODE
                "
            ;;
        "n11"|"n12"|"n13"|"n14"|"n15"|"n16")
            vcmd -c "/tmp/pycore.${PROCESS_ID}/${NODE}" -- bash -c "
                $CUSTOM_COMMAND_INIT_CLIENT
                "
            ;;
        "n17"|"n24")
            vcmd -c "/tmp/pycore.${PROCESS_ID}/${NODE}" -- bash -c "
                $CUSTOM_COMMAND_INIT_CLIENT
                "
            ;;
    esac
done


# Add sleep time (e.g., 1 second)
sleep 1

# Run the final vcmd command
vcmd -c "/tmp/pycore.${PROCESS_ID}/n7" -- bash -c "
    cp -r ${SOURCE_FOLDER}/Testing/* .
    ls
    "
sleep 1


# Open terminal for SERVER 1 - n17
xterm -T "Server 1 N17" -geometry 80x24+0+0 -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n17' -- bash -c 'python3 Server.py 6000'; exec bash" &

# Open terminal for SERVER 1 - n24
xterm -T "Server 2 N24" -geometry 80x24+0+300 -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n24' -- bash -c 'python3 Server.py 6000'; exec bash" &

#
sleep 1

# Open terminal for NODERP - n7
xterm -T "NodeRP N7" -geometry 80x24+400+0 -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n7' -- bash -c 'python3 NodeRP.py 5000'; exec bash" &

sleep 1

# Open terminal for Node 1 - n1
xterm -T "Node 1" -geometry 80x24+800+0 -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n1' -- bash -c 'python3 Node.py 5000 1 10.0.7.2'; exec bash" &

sleep 1

# # Open terminal for Node 26 - n26
# xterm -T "Node 26" -geometry 80x24+1200+0 -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n25' -- bash -c 'python3 Node.py 5000 25 10.0.7.2'; exec bash" &

# sleep 1
# # Send a LOCATE_RP through a test_locate_rp
# xterm -T "TESTING LOCATE_RP" -geometry 80x24+1200+300 -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n26' -- bash -c 'python3 test_locate_rp.py 10.0.14.1'; exec bash " & 


# Open terminal for Node 13 - n13 ( TEST CLIENT REQUEST )
xterm -T "Client N13" -geometry 80x24+800+400 -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n13' -- bash -c 'python3 connect_to_node.py 10.0.1.1'; exec bash" &

sleep 6

# Open terminal for Node 10 - n10 
xterm -T "Node 10" -geometry 80x24+1400+0 -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n10' -- bash -c 'python3 Node.py 5000 10 10.0.8.1'; exec bash" &

sleep 1
# Open terminal for Node 16 - n16 ( TEST CLIENT REQUEST )
xterm -T "Client N16" -geometry 80x24+1400+400 -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n16' -- bash -c 'python3 connect_to_node.py 10.0.2.1'; exec bash" &

sleep 2

# Open terminal for Node 14 - n14 ( TEST CLIENT REQUEST DIRECTLY TO NODERP)
xterm -T "Client N14" -geometry 80x24+1400+800 -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n14' -- bash -c 'python3 connect_to_node.py 10.0.5.1'; exec bash" &

sleep 10

# Open terminal for Node 12 - n12 ( TEST CLIENT REQUEST )
xterm -T "Client N12" -geometry 80x24+800+800 -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n13' -- bash -c 'python3 connect_to_node.py 10.0.1.1'; exec bash" &


# sleep 5

# xterm -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n14' -- bash -c 'python3 testClient.py'; exec bash" &

# sleep 1

# xterm -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n18' -- bash -c 'python3 testClient.py'; exec bash" &


# Wait for all background jobs to finish
wait    