#!/bin/bash
args="";
i=1;
for arg in "$@" 
do
    args=$args" "$arg;
    i=$((i + 1));
done
timeout --signal=SIGINT 5m /usr/bin/yt-dlp --cookies cookies.txt $args > /dev/null 2>&1
