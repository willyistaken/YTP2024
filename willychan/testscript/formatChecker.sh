#!/bin/bash

DIR=$1
ERROR_LOG="error_log.txt"

if [ -z "$DIR" ]; then
	echo "Usage: $0 <directory>"
	exit 1
fi

> "$ERROR_LOG"

find "$DIR" -type f -name "*.txt" | while read -r file; do
	base="${file%.txt}"
	mid_file="${base}.mid"
	if ./a.out "$file" "$file" 2>> "$ERROR_LOG" ; then
		echo "succes"
	else
		echo "failed"
		mv "$file" failedtrack/.
		mv "$mid_file" failedtrack/.

	fi
done
