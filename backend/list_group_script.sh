#!/bin/bash

# File to read users from
group_file="/etc/group"

# UID threshold, usually 1000, but can vary by distribution
gid_threshold=1000

# Flag for User private group
UPG=false

# Process options
while getopts ":r" opt; do
    case ${opt} in
        r )
            UPG=true
            ;;
        \? )
            echo "Invalid option: $OPTARG" 1>&2
            exit 1
            ;;
    esac
done

# Shift processed options away
shift $((OPTIND -1))

# Check if the -r option was provided
if [ "$UPG" = true ]; then
    # List regular users (UID >= threshold)
    awk -F: -v threshold="$gid_threshold" '$3 >= threshold {print $1}' "$group_file"
else
    # List system users (UID < threshold)
    awk -F: -v threshold="$gid_threshold" '$3 < threshold {print $1}' "$group_file"
fi
