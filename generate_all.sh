#!/bin/sh

rm wget.log

while read version; do
    echo "Generate $version"

    wget https://www.prestashop.com/download/old/prestashop_$version.zip -O ./extracts/prestashop.zip
    if [ $? = 0 ]; then
        unzip ./extracts/prestashop.zip -d ./extracts/

        docker build -t quetzacoalt/prestashop:$version .

        rm -rf ./extracts/*
        docker push quetzacoalt/prestashop:$version
    else
        echo "Failed to download $version" >> wget.log
    fi
done <versions.txt
