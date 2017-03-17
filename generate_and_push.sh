#!/bin/bash

php_version_default="5.6"

generate_image()
{
    echo "Generate Dockerfile for PrestaShop $version - PHP $php_version"

    if [ "$php_version_default" = "$php_version" ]; then
        folder="$version";
    else
        folder="${version:0:3}-$php_version";
    fi

    mkdir -p images/$folder/

    sed  '
            s/{PS_VERSION}/'"$version"'/;
            s/{PHP_VERSION}/'"$php_version"'/;
            s/{PS_URL}/'"https:\/\/www.prestashop.com\/download\/old\/prestashop_$version.zip"'/
        ' Dockerfile.model > images/$folder/Dockerfile

    cp -R config_files/ images/$folder/
}

if [ -z "$1" ]; then
    ps_versions_file="versions.txt";
else
    ps_versions_file="$1";
fi

# Generate images for all PrestaShop versions from 1.4 on PHP 5.6
php_version=$php_version_default
echo "Reading versions in $ps_versions_file ..."
while read version; do
    generate_image
done <$ps_versions_file

# Generate images for each major version of PrestaShop on different PHP environment
for php_version in "5.5" "7.0"
do

    for major_version in "15" "16" "17"
    do
        version=$(grep "." versions$major_version.txt | tail -1)
        generate_image
    done

done
