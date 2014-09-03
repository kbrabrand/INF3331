#!/bin/bash

# Get argument cound
argNum=$#;

# Return usage hint if we didn't get enough arguments
if [ "$argNum" -lt 2 ]
then
    echo "usage: sized_delete.sh path size";
    exit 1
else
    # Set provided path and file size as variables
    path=$1;
    size=$2;

    # Execute find command and grep for a string in all matches
    response=$(find $path -type f -size +"$size"k -exec ls {} \; -delete);

    # Return command output if non-empty string, informative string if not
    if [[ -n $response ]]; then
        echo "Deleting..."
        echo "$response"
    else
        echo "No files of size larger than $size kilobytes found"
    fi
fi