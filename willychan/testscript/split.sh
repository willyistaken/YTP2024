#!/bin/bash

SOURCE_DIR="$1"  # Directory containing files
NS_DIR="$1/ns_files"  # Folder for files containing "NS"
OTHER_DIR="$1/normal_files"  # Folder for other files
FAIL_DIR="$1/fail_files"

# Create destination folders if they don't exist
mkdir -p "$NS_DIR" "$OTHER_DIR" "$FAIL_DIR"

# Iterate over files in SOURCE_DIR
find "$SOURCE_DIR" -type f -name "*.txt" | while read -r file; do
	./a.out "$file" "$file" > /dev/null 2>&1
	if [[ $? -eq 0 ]]; then
		if [[ "$(basename "$file")" == *NS* ]]; then
			mv "${file%.txt}.mid" "$NS_DIR/"
			mv "$file" "$NS_DIR/"
    	else
			mv "${file%.txt}.mid" "$OTHER_DIR/"
			mv "$file" "$OTHER_DIR/"
    	fi
	else
		echo "Program execution failed.,moved to failed"
		mv "${file%.txt}.mid" "$FAIL_DIR/"
		mv "$file" "$FAIL_DIR/"
	fi

    done

echo "Files have been sorted!"

