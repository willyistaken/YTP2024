#!/bin/bash

DIR=$1
ERROR_LOG="error_log.txt"

if [ -z "$DIR" ]; then
	echo "Usage: $0 <directory>"
	exit 1
fi

> "$ERROR_LOG"

# find "$DIR" -type f -name "*.txt" | while read -r file; do
# 	./a.out "$file" "$file" 2>> "$ERROR_LOG"
# done

find "$DIR" -type f -name "*.txt" | while read -r file; do
	./armc.out "$file" "$file" 2>> "$ERROR_LOG"
done

