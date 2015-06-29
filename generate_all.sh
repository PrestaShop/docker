#!/bin/sh

while read version; do
  echo "Generate $version"

  wget https://www.prestashop.com/download/old/prestashop_$version.zip -O ./extracts/prestashop.zip
  unzip ./extracts/prestashop.zip -d ./extracts/

  docker build -t quetzacoalt/prestashop:$version .

  rm -rf ./extracts/*
done <versions.txt

docker push quetzacoalt/prestashop
