#!/bin/bash
if  [ $# -eq 0 ]
then
	echo "Input the pack id (contained in the URL as the categoryid, example : https://zenius-i-vanisher.com/v5.2/viewsimfilecategory.php?categoryid=34)";
    return 1;
else
	id=$1;
	ver=$2;
fi
	mkdir -p data;
	cd data;

    file=${ver}.zip
    uri=$(curl https://zenius-i-vanisher.com/v5.2/viewsimfilecategory.php?categoryid=$id | 
    grep 'class="fb"' | grep 'download.php?' | sed -nE 's/.*href="([^"]+).*/https\:\/\/zenius\-i\-vanisher\.com\/v5\.2\/\1/p' |
    sed -ne 's/amp;//p')
    echo $uri
    echo downloading to $file

    if test -e "$file"
    then zflag=(-z "$file")
    else zflag=()
    fi
    curl -L -J $uri -o $file ${zflag[@]}

