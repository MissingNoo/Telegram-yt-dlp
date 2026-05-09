#!/bin/bash
args="";
i=1;
for arg in "$@" 
do
    args=$args" "$arg;
    i=$((i + 1));
done
echo $args
timeout 3m yt-dlp --js-runtimes deno --remote-components ejs:github --cookies-from-browser firefox $args -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" #> /dev/null 2>&1
