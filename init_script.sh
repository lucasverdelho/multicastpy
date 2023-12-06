#!/bin/bash

# Set the process ID
PROCESS_ID="36725"

# List of nodes for which you want to run vcmd commands
NODES=("n1" "n2" "n3" "n4" "n5" "n6" "n7" "n8" "n9" "n10" "n11" "n12" "n13" "n14" "n15" "n16" "n17" "n18" "n24") 

# Source folder for file copies
SOURCE_FOLDER="/home/core/multicastpy"

# Your custom commands
CUSTOM_COMMAND_INIT_NODE="ls"
CUSTOM_COMMAND_INIT_CLIENT="echo 'Hello from Node (Client)'"
CUSTOM_COMMAND_INIT_SERVER="python3 Server.py 6000"

# Iterate over nodes and run vcmd commands
for NODE in "${NODES[@]}"; do
    vcmd -c "/tmp/pycore.${PROCESS_ID}/${NODE}" -- bash -c "
        cp ${SOURCE_FOLDER}/Testing/neighbour_lists/* .
        "
    case $NODE in
        "n1"|"n2"|"n5"|"n10") # Overlay Nodes
            vcmd -c "/tmp/pycore.${PROCESS_ID}/${NODE}" -- bash -c "
                cp ${SOURCE_FOLDER}/Testing/*.py .
                "
            ;;
        "n11"|"n12"|"n13"|"n14"|"n15"|"n16"|"n18")
            vcmd -c "/tmp/pycore.${PROCESS_ID}/${NODE}" -- bash -c "
                cp ${SOURCE_FOLDER}/Testing/Client.py .
                cp ${SOURCE_FOLDER}/Testing/RtpPacket.py .
                cp ${SOURCE_FOLDER}/Testing/VideoStream.py .
                cp ${SOURCE_FOLDER}/Testing/testClient.py .
                cp ${SOURCE_FOLDER}/Testing/testNode.py .
                cp ${SOURCE_FOLDER}/Testing/connect_to_test_node.py .
                cp ${SOURCE_FOLDER}/Testing/connect_to_node.py .
                "
            ;;
        "n17"|"n24")
            vcmd -c "/tmp/pycore.${PROCESS_ID}/${NODE}" -- bash -c "
                cp ${SOURCE_FOLDER}/Testing/Server.py .
                cp ${SOURCE_FOLDER}/Testing/ServerWorker.py .
                cp ${SOURCE_FOLDER}/Testing/VideoStream.py .
                cp ${SOURCE_FOLDER}/Testing/RtpPacket.py .
                mkdir -p content  # Create 'content' folder if it doesn't exist
                cp ${SOURCE_FOLDER}/Testing/movie.Mjpeg content/.
                "
            ;;
    esac
done

sleep 1

# Iterate over nodes and run vcmd commands for custom initialization commands
for NODE in "${NODES[@]}"; do
    case $NODE in
        "n1"|"n2"|"n5"|"n10")
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
    "
sleep 1


# Open terminal for n17 using xterm ----- SERVER 1 -----
xterm -geometry 80x24+0+0 -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n17' -- bash -c 'python3 Server.py 6000'; exec bash" &

# xterm -geometry 80x24+1400+0 -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n24' -- bash -c 'python3 Server.py 6000'; exec bash" &

sleep 1

# Open terminal for n7 using xterm ----- NODERP -----
xterm -geometry 80x24+400+0 -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n7' -- bash -c 'python3 NodeRP.py 5000'; exec bash" &

sleep 1


xterm -geometry 80x24+800+0 -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n1' -- bash -c 'python3 Node.py 5000 1 10.0.7.2'; exec bash" &

sleep 2

xterm -geometry 80x24+800+450 -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n13' -- bash -c 'python3 connect_to_node.py 10.0.1.1'; exec bash" &


# Open terminal for n14 using xterm
# xterm -geometry 80x24+800+0 -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n14' -- bash -c 'python3 testNode.py 10.0.5.1 5000 movie.Mjpeg'; exec bash" &

# sleep 1

# xterm -geometry 80x24+0+400 -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n14' -- bash -c 'python3 connect_to_test_node.py 127.0.0.1 7770'; exec bash" &

# sleep 6

# xterm -geometry 80x24+800+400 -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n18' -- bash -c 'python3 testNode.py 10.0.5.1 5000 movie.Mjpeg'; exec bash" &

# sleep 1

# xterm -geometry 80x24+0+1200 -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n18' -- bash -c 'python3 connect_to_testNode.py 127.0.0.1 7770'; exec bash" &



# sleep 5

# xterm -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n14' -- bash -c 'python3 testClient.py'; exec bash" &

# sleep 1

# xterm -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n18' -- bash -c 'python3 testClient.py'; exec bash" &


# Wait for all background jobs to finish
wait    