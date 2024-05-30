#!/bin/bash

for f in data/*.zip; do
    # zip -d $f "*.avi" "*.ogg" || [ $? -eq 12 ];
    unzip -uo "$f" "*.sm" "*.ssc" "*.png" -d "$(echo $f | sed -e 's/\.zip//')" || [ $? -eq 9 ];
done
