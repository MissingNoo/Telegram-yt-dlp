#!/bin/bash
args="";
i=1;
for arg in "$@" 
do
    args=$args" "$arg;
    i=$((i + 1));
done
echo $args
timeout 5m /home/airgeadlamh/.local/bin/yt-dlp $args #> /dev/null 2>&1
