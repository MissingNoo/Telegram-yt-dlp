#!/bin/bash
args="";
i=1;
for arg in "$@" 
do
    args=$args" "$arg;
    i=$((i + 1));
done
timeout 5m /usr/bin/yt-dlp -f "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]" $args > /dev/null 2>&1