#!/bin/sh

if [ -z "$1" ]; then
    ps_versions_file="versions.txt";
else
    ps_versions_file="$1";
fi

echo "Reading verions in $ps_versions_file ..."

while read version; do
    echo "Generate Dockerfile for PrestaShop $version"

    mkdir -p images/$version/

    sed  '
			s/{PS_VERSION}/'"$version"'/;
			s/{PS_URL}/'"https:\/\/www.prestashop.com\/download\/old\/prestashop_$version.zip"'/
		' Dockerfile.model > images/$version/Dockerfile

    cp -R config_files/ images/$version/

    #docker build -t prestashop/prestashop:$version images/$version/
    #docker push quetzacoalt/prestashop:$version
done <$ps_versions_file
