#! /usr/bin/bash

midfile=$1
txtfile=$2

python ../algo/greedy.py $midfile > $txtfile
python ../algo/gagademo.py $midfile > $txtfile
