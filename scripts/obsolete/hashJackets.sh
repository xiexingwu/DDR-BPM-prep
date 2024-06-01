#!/bin/bash
while IFS= read -r line; do
    file="./jackets-lowres/${line}-jacket.png"
    if [[ ! -f $file ]]; then
        echo "$file not found" 1>&2
    else
        bash ./bin/hash.sh "$file"
    fi
done < all_songs.txt
