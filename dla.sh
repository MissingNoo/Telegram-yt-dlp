#!/bin/bash
args="";
i=1;
for arg in "$@" 
do
    args=$args" "$arg;
    i=$((i + 1));
done
echo $args
/usr/bin/yt-dlp --extract-audio --audio-format mp3 $args;