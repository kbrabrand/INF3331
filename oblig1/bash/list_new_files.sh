#!/bin/bash

# Get argument cound
argNum=$#;

# Return usage hint if we didn't get enough arguments
if [ "$argNum" -lt 2 ]
then
    echo "usage: list_new_files.sh path days";
    exit 1
else
    # Set path and days arguments as variables to improve readability
    path=$1;
    days=$2;

    # Check if the days parameter is an integer
    re='^[0-9]+$'
    if ! [[ $days =~ $re ]] ; then
       echo "error: Day parameter is not an integer" >&2;
       exit 1
    fi

    # Use find to
    # 1. find files changed during the last $days days
    # 2. get the size for each of the matched files
    # 3. sort the list of files in ascending order
    find $path -type f -mtime -$days -print0 | xargs -0 du -skh | sort -n
fi