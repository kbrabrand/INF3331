#!/bin/bash

# Get argument cound
argNum=$#;

# Return usage hint if we didn't get enough arguments
if [ "$argNum" -lt 2 ]
then
    echo "usage: sort_file.sh source destionation";
    exit 1
else
    # Set file and destination file as variables
    source=$1;
    destination=$2;

    # Sort source file and output to destination
    sort $source -o $destination
fi