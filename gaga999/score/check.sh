#!/bin/bash

# mid_file=$1
# txt_file="${mid_file%.mid}.txt"

echo 1 > result.txt
# ./a.out "$txt_file" temp.txt >> result.txt
./armc.out text.txt temp.txt >> result.txt
# ./armc.out "$txt_file" temp.txt >> result.txt
    

echo 0 >> result.txt
# cat "$txt_file" > text.txt

python3 average.py < result.txt