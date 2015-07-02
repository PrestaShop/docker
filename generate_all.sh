#!/bin/sh

while read version; do
    echo "Generate Dockerfile for PrestaShop $version"

    mkdir -p images/$version/

    sed  '
			s/{PS_VERSION}/'"$version"'/;
			s/{PS_URL}/'"https:\/\/www.prestashop.com\/download\/old\/prestashop_$version.zip"'/
		' Dockerfile.model > images/$version/Dockerfile

    cp -R config_files/ images/$version/
done <versions.txt
