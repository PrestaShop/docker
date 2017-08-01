#!/bin/bash

folder=$1

if [[ -n "$folder" ]]; then  

    # dwl version contains zip file with tree structure (1.7)
    if [ ! -d $folder/prestashop ]; then
        unzip -n -q $folder/prestashop.zip -d $folder/prestashop
	rm -rf $folder/prestashop.zip	
    fi

    # prepair tree structure for volumes
    mv $folder/prestashop/themes $folder/prestashop/modules $folder/prestashop/override $folder/

    # build relative symlinks for volumes
    ln -s ../themes $folder/prestashop/themes
    ln -s ../modules $folder/prestashop/modules
    ln -s ../override $folder/prestashop/override
else
    echo "Missing folder to move"
fi
