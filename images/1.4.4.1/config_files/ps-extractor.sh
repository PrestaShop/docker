#!/bin/bash

folder=$1
destination="/var/www/html"

if [[ -n "$folder" ]]; then
    if [ -d $folder/prestashop ]; then
        cp -n -R $folder/prestashop/* $destination
    else
        unzip -n -q $folder/prestashop.zip -d $destination
    fi
else
    echo "Missing folder to move"
fi
