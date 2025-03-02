#! /usr/bin/bash
out_path_mid=$1
mp3path=$2

basic-pitch . $mp3path

midfile=$(basename $mp3path)
midfile="${midfile::-4}""_basic_pitch.mid"

mv $midfile $out_path_mid

