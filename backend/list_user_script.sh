#!/bin/bash

# File to read users from
passwd_file="/etc/passwd"

# UID threshold, usually 1000, but can vary by distribution
uid_threshold=1000

# Flag for regular users
regular_users=false

# Process options
while getopts ":r" opt; do
    case ${opt} in
        r )
            regular_users=true
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
if [ "$regular_users" = true ]; then
    # List regular users (UID >= threshold)
    awk -F: -v threshold="$uid_threshold" '$3 >= threshold {print $1}' "$passwd_file"
else
    # List system users (UID < threshold)
    awk -F: -v threshold="$uid_threshold" '$3 < threshold {print $1}' "$passwd_file"
fi
