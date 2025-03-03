#!/bin/bash

for file in libs/*.mid; do
python3 algo.py "$file"
done