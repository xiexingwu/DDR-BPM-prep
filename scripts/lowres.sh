#!/bin/bash

mkdir -p $(BUILD_DIR)/jackets-160

for f in build/jackets/*.png; do
    mogrify -resize 160x160 -quality 100 -path 
# OIFS="$IFS"
# IFS=$'\n'
#
# cd ./jackets
# for f in `find . -type f -name "*.png"`; do
# 	# echo "$f"; 
# 	if [[ ! -f "../jackets-lowres/$f" ]]; then 
# 		mogrify -resize 128x128 -quality 100 -path ../jackets-lowres "$f"; 
# 	fi
# done
