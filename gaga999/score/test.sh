#!/bin/bash

mid_file=$2
txt_file="${mid_file%.mid}.txt"
python3 "$1" "$mid_file" > temp.txt
if [[ $? -eq 0 ]]; then
    echo 1 > result.txt
    # ./a.out "$txt_file" temp.txt >> result.txt
    ./armc.out "$txt_file" temp.txt >> result.txt
    # ./armc.out "$txt_file" temp.txt >> result.txt
    
    if [[ $? -eq 0 ]]; then
        :
    else
        echo "$txt_file";
    fi	
else
    echo "$txt_file";
fi

echo 0 >> result.txt
cat "$txt_file" > text.txt

python3 average.py < result.txt


