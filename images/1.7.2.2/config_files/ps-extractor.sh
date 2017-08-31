#!/bin/bash

folder=$1

if [[ -n "$folder" ]]; then

    # dwl version contains zip file with tree structure (1.7)
    if [ ! -d $folder/prestashop ]; then
        unzip -n -q $folder/prestashop.zip -d $folder/prestashop
        rm -rf $folder/prestashop.zip
    fi

    cp -n -R $folder/prestashop/* /var/www/html
else
    echo "Missing folder to move"
fi
