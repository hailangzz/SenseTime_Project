#!/bin/bash

file=$1
size=$(stat -c%s "$file")
duration=$(ffprobe -v error -select_streams v:0 -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$file")

bitrate=$(echo "$size * 8 / $duration / 1000" | bc)

echo "Video Bitrate: $bitrate kbps"

