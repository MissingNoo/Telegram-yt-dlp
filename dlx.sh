#!/bin/bash
args="";
i=1;
for arg in "$@" 
do
    args=$args" "$arg;
    i=$((i + 1));
done
timeout 5m /usr/bin/yt-dlp $args > /dev/null 2>&1
