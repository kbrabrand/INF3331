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

    # Use find to
    # 1. find files changed during the last $days days
    # 2. get the size for each of the matched files
    # 3. sort the list of files in ascending order
    find $path -type f | xargs grep $word -n
fi