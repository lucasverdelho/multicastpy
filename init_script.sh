#!/bin/bash

# Set the process ID
PROCESS_ID="38297"

# List of nodes for which you want to run vcmd commands
NODES=("n1" "n2" "n3" "n4" "n5" "n6" "n7" "n8" "n9" "n10" "n11" "n12" "n13" "n14" "n15" "n16" "n17")

# Source folder for file copies
SOURCE_FOLDER="/home/core/multicastpy"

# Your custom commands
CUSTOM_COMMAND_INIT_NODE="ls"
CUSTOM_COMMAND_INIT_CLIENT="echo 'Hello from Node (Client)'"
CUSTOM_COMMAND_INIT_SERVER="echo 'Hello from Node (Server)'"

# Iterate over nodes and run vcmd commands
for NODE in "${NODES[@]}"; do
    vcmd -c "/tmp/pycore.${PROCESS_ID}/${NODE}" -- bash -c "
        cp ${SOURCE_FOLDER}/netconfig.txt .
        "
    case $NODE in
        "n1"|"n2"|"n3"|"n4"|"n5"|"n6"|"n7"|"n8"|"n9"|"n10")
            vcmd -c "/tmp/pycore.${PROCESS_ID}/${NODE}" -- bash -c "
                cp ${SOURCE_FOLDER}/node.py .
                "
            ;;
        "n11"|"n12"|"n13"|"n14"|"n15"|"n16")
            vcmd -c "/tmp/pycore.${PROCESS_ID}/${NODE}" -- bash -c "
                cp ${SOURCE_FOLDER}/client.py .
                "
            ;;
        "n17")
            vcmd -c "/tmp/pycore.${PROCESS_ID}/${NODE}" -- bash -c "
                cp ${SOURCE_FOLDER}/server.py .
                "
            ;;
    esac
done


# Iterate over nodes and run vcmd commands for custom initialization commands
for NODE in "${NODES[@]}"; do
    case $NODE in
        "n1"|"n2"|"n3"|"n4"|"n5"|"n6"|"n7"|"n8"|"n9"|"n10")
            vcmd -c "/tmp/pycore.${PROCESS_ID}/${NODE}" -- bash -c "
                $CUSTOM_COMMAND_INIT_NODE
                "
            ;;
        "n11"|"n12"|"n13"|"n14"|"n15"|"n16")
            vcmd -c "/tmp/pycore.${PROCESS_ID}/${NODE}" -- bash -c "
                $CUSTOM_COMMAND_INIT_CLIENT
                "
            ;;
        "n17")
            vcmd -c "/tmp/pycore.${PROCESS_ID}/${NODE}" -- bash -c "
                $CUSTOM_COMMAND_INIT_SERVER
                "
            ;;
    esac
done