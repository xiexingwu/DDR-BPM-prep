#!/bin/bash
SEED_DIR=${SEED_DIR:-./data}

for f in $SEED_DIR/*.zip; do
    unzip -uo "$f" "*.sm" "*.ssc" "*.png" -d "$(echo $f | sed -e 's/\.zip//')" || [ $? -eq 1 || $? -eq 9 ];
done
