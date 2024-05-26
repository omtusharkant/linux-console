#!/bin/bash

# File to read users from
passwd_file="/etc/passwd"

# UID threshold, usually 1000, but can vary by distribution
uid_threshold=1000


awk -F: -v threshold="$uid_threshold" '$3 < threshold {print $1}' "$passwd_file"

