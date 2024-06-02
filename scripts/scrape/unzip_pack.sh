#!/bin/bash
SEED_DIR=${SEED_DIR:-./data}

for f in $SEED_DIR/*.zip; do
    # zip -d $f "*.avi" "*.ogg" || [ $? -eq 12 ];
    unzip -uo "$f" "*.sm" "*.ssc" "*.png" -d "$(echo $f | sed -e 's/\.zip//')" || [ $? -eq 9 ];
done
