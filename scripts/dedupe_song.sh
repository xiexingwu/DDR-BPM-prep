#!/bin/bash
if  [ $# -ne 2 ]
then
    echo "Input the song name and version (folder name) to delete";
    exit 1;
else
	name=$1;
	ver=$2;
fi

rm -rfv "data/$ver/$name"
