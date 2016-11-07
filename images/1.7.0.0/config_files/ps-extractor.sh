#!/bin/bash

folder=$1
destination="/var/www/html"

if [[ -n "$folder" ]]; then
    if [ -d $folder/prestashop ]; then
       mv -v $folder/prestashop/* $destination
    else
        unzip -q $folder/prestashop.zip -d $destination
    fi
else
    echo "Missing folder to move"
fi
