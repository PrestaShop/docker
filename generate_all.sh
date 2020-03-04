#!/bin/bash

# Decalre globals variables
PHP_DEFAULT_VERSION="5.6-apache"
if [ -z "$1" ]; then
    PS_VERSIONS_FILE="versions.txt";
else
    PS_VERSIONS_FILE="$1";
fi

generate_image()
{
    local php_version=$1
    local version=$2
    local folder=""

    echo "Generate Dockerfile for PrestaShop ${version} - PHP ${php_version}"
    if [ "${php_version}" = "" ]; then
        folder="${version}";
        php_version=$PHP_DEFAULT_VERSION
    elif [ "${version}" = "nightly" ]; then
        folder="${version}-${php_version}";
    else
        folder="${version:0:3}-${php_version}";
    fi

    mkdir -p images/$folder/

    if [ $version = "nightly" ]; then
        sed '
                s/{PS_VERSION}/'"${version}"'/;
                s/{PHP_VERSION}/'"${php_version}"'/
            ' Dockerfile-nightly.model > images/$folder/Dockerfile
    else
        sed '
                s/{PS_VERSION}/'"${version}"'/;
                s/{PHP_VERSION}/'"${php_version}"'/;
                s/{PS_URL}/'"https:\/\/www.prestashop.com\/download\/old\/prestashop_$version.zip"'/
            ' Dockerfile.model > images/$folder/Dockerfile
    fi
}

parse_versions()
{
    # Generate images for each major VERSION of PrestaShop on different PHP environment
    for php_version in $1; do
        for major_version in $2; do
            version=$(grep "." "versions${major_version}.txt" | tail -1)
            generate_image $php_version $version
        done
    done
}

# Generate images for all PrestaShop versions from 1.4 on PHP 5.6
echo "Reading versions in $PS_VERSIONS_FILE ..."
while read version; do
    generate_image "" $version
done < $PS_VERSIONS_FILE

# Specific to old PrestaShop versions
PHP_VERSION=("5.6-apache" "7.0-apache" "7.1-apache" "5.6-fpm" "7.0-fpm" "7.1-fpm")
MAJOR_VERSION=("15" "16")
parse_versions $PHP_VERSION $MAJOR_VERSION

# Used for 1.7 and nightly versions
PHP_VERSION=("7.1-apache" "7.2-apache" "7.3-apache" "7.1-fpm" "7.2-fpm" "7.3-fpm")
MAJOR_VERSION=("17" "nightly")
parse_versions $PHP_VERSION $MAJOR_VERSION
