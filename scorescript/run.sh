
#!/bin/bash

# Check if the user provided a folder argument
if [[ -z "$1" ]]; then
    echo "Usage: $0  <program>"
    exit 1
fi

# Assign the folder path
folder="libs"

# Check if the folder exists
if [[ ! -d "$folder" ]]; then
    echo "Error: Folder '$folder' not found."
    exit 1
fi

# Iterate through .mid files in the specified folder
rm result.txt
for mid_file in "$folder"/*.mid; do
    # Check if any .mid files exist
    [[ -e "$mid_file" ]] || continue

    txt_file="${mid_file%.mid}.txt"


	#CHANGE HERE , whatever your program do here, just output it to temp.txt, $1 is your program(which is the argument this script take)
    python $1 $mid_file > temp.txt

	
	if [[ $? -eq 0 ]]; then
		echo 1 >> result.txt
		./a.out "$txt_file" temp.txt >> result.txt
		
		if [[ $? -eq 0 ]]; then
			:
		else
			echo "$txt_file";
		fi	
	else
		echo "$txt_file";
	fi
	
done
echo 0 >> result.txt

python average.py < result.txt

