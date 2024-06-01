#!/bin/bash
SEED_DIR=${SEED_DIR:-./data}

if  [ $# -ne 2 ]
then
	echo "Input the song id (contained in the URL as the categoryid, example : https://zenius-i-vanisher.com/v5.2/viewsimfile.php?simfileid=38006)";
    exit 1;
else
	id=$1;
	ver=$2;
fi

mkdir -p $SEED_DIR/$ver;
cd $SEED_DIR/$ver;

title=$(curl https://zenius-i-vanisher.com/v5.2/viewsimfile.php?simfileid=$id | grep "<h1>" | (sed -e 's/<h1>//' -e 's/<\/h1>//') | sed -e 's: /.*::');
file=${title}.zip
uri="https://zenius-i-vanisher.com/v5.2/download.php?type=ddrsimfile&simfileid=$id"

echo $uri
echo downloading to $file

if test -e "$file"
then zflag=(-z "$file")
else zflag=()
fi
curl -L -J $uri -o "$file" ${zflag[@]}

unzip -uo "$file" "*.sm" "*.ssc" "*.png" || [ $? -eq 9 ]
