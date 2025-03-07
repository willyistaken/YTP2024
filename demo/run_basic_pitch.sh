#! /usr/bin/bash
out_path_mid=$1
mp3path=$2

basic-pitch . $mp3path

midfile=$(basename $mp3path)
midfile="${midfile::-4}""_basic_pitch.mid"

python3 fixmidi.py $midfile 3
mv "${midfile::-4}""2.mid" $out_path_mid
rm $midfile

