#!/bin/bash
OIFS="$IFS"
IFS=$'\n'

cd ./jackets
for f in `find . -type f -name "*.png"`; do
	# echo "$f"; 
	if [[ ! -f "../jackets-lowres/$f" ]]; then 
		mogrify -resize 128x128 -quality 100 -path ../jackets-lowres "$f"; 
	fi
done