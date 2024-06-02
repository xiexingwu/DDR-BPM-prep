#!/bin/bash
SEED_DIR=${SEED_DIR:-./data}
BUILD_DIR=${BUILD_DIR:-./build}

jackets_dir=$BUILD_DIR/jackets-160
mkdir -p $jackets_dir

OIFS="$IFS"
IFS=$'\n'
while IFS= read -r name; do
    [[ -f "$jackets_dir/$name.png" && -z $FORCE ]] && continue

    search_name=$(echo $name | sed -e 's:\[:\\[:g' -e 's:]:\\]:g') # escape square brackets
    png=$(find $SEED_DIR -type f -name "$search_name-jacket.png")
    [[ -z $png || ${#png[@]} -eq 0 ]] && echo "$name jacket not found" && exit 1
    [[ ${#png[@]} -gt 1 ]] && echo "Multiple found for $name:\n\t$png" && exit 1

    echo Downsizing $name from $png
    convert "$png" -resize 160x160 -quality 100 "$jackets_dir/$name.png"
done < $SEED_DIR/all_songs.txt
