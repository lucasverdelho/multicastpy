#!/bin/bash

# Set the process ID
PROCESS_ID="43101"

# List of nodes for which you want to run vcmd commands
NODES=("n1" "n2" "n3" "n4" "n5" "n6" "n7" "n8" "n9" "n10" "n11" "n12" "n13" "n14" "n15" "n16" "n17" "n18") 

# Source folder for file copies
SOURCE_FOLDER="/home/core/multicastpy"


# Open terminal for n17 using xterm
xterm -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n17' -- bash -c 'python3 Server.py 6000'; exec bash" &

sleep 1

# Open terminal for n7 using xterm
xterm -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n7' -- bash -c 'python3 NodeRP.py 5000'; exec bash" &

sleep 1

# Open terminal for n14 using xterm
xterm -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n14' -- bash -c 'python3 testNode.py 10.0.5.1 5000 movie.Mjpeg'; exec bash" &


sleep 5

xterm -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n14' -- bash -c 'python3 testClient.py'; exec bash" &

sleep 1

xterm -e "vcmd -c '/tmp/pycore.${PROCESS_ID}/n18' -- bash -c 'python3 testClient.py'; exec bash" &

# Wait for all background jobs to finish
wait    