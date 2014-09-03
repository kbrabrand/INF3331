#!/bin/bash

# Get argument cound
argNum=$#;

# Return usage hint if we didn't get enough arguments
if [ "$argNum" -lt 2 ]
then
    echo "usage: find_word.sh path word";
    exit 1
else
    # Set path and days arguments as variables to improve readability
    path=$1;
    word=$2;

    # Execute find command and grep for a string in all matches
    response=$(find $path -type f | xargs grep $word -n);

    # Return command output if non-empty string, informative string if not
    if [[ -n $response ]]; then
        echo "$response"
    else
        echo "No files containing \"$word\" found"
    fi
fi