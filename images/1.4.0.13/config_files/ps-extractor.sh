#!/bin/bash

folder=$1
destination="/var/www/html"

if [[ -n "$folder" ]]; then
    if [ -d $folder/prestashop ]; then
       mv -v $folder/prestashop/* $destination
    else
        mv -v $folder/prestashop.zip $folder/index.php $destination
    fi
else
    echo "Missing folder to move"
fi
