#!/bin/bash

# Decalre globals variables
PHP_DEFAULT_VERSION="5.6-apache"
NEW_PHP_DEFAULT_VERSION="7.1-apache"
WHEN_PHP_WAS_UPGRADED=1.7.6
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
    local php_url=""

    echo "Generate Dockerfile for PrestaShop ${version} - PHP ${php_version}"
    if [ "${php_version}" = "" ]; then
        folder="${version}";
        version_compare $version $WHEN_PHP_WAS_UPGRADED
        if [ $? = 2 ]; then
            php_version=$PHP_DEFAULT_VERSION
        else
            php_version=$NEW_PHP_DEFAULT_VERSION
        fi
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
        ps_url="https:\\/\\/www.prestashop.com\\/download\\/old\\/prestashop_${version}.zip"

        sed '
                s/{PS_VERSION}/'"${version}"'/;
                s/{PHP_VERSION}/'"${php_version}"'/;
                s/{PS_URL}/'"${ps_url}"'/
            ' Dockerfile.model > images/$folder/Dockerfile
    fi
}

version_compare()
{
    if [[ $1 == $2 ]]
    then
        return 0
    fi
    local IFS=.
    local i ver1=($1) ver2=($2)
    # fill empty fields in ver1 with zeros
    for ((i=${#ver1[@]}; i<${#ver2[@]}; i++))
    do
        ver1[i]=0
    done
    for ((i=0; i<${#ver1[@]}; i++))
    do
        if [[ -z ${ver2[i]} ]]
        then
            # fill empty fields in ver2 with zeros
            ver2[i]=0
        fi
        if ((10#${ver1[i]} > 10#${ver2[i]}))
        then
            return 1
        fi
        if ((10#${ver1[i]} < 10#${ver2[i]}))
        then
            return 2
        fi
    done
    return 0
}

# Generate images for all PrestaShop versions from 1.4 on PHP 5.6
echo "Reading versions in $PS_VERSIONS_FILE ..."
while read version; do
    generate_image "" $version
done < $PS_VERSIONS_FILE

# Specific to old PrestaShop versions
echo "Reading versions in versions15.txt and versions16.txt ..."
PHP_VERSION=("5.6-apache" "7.0-apache" "7.1-apache" "5.6-fpm" "7.0-fpm" "7.1-fpm")
MAJOR_VERSION=("15" "16")
# Generate images for each major VERSION of PrestaShop on different PHP environment
for php_version in ${PHP_VERSION[@]}; do
    for major_version in ${MAJOR_VERSION[@]}; do
        version=$(grep "." "versions${major_version}.txt" | tail -1)
        generate_image $php_version $version
    done
done

# Used for 1.7 and nightly versions
echo "Reading versions in versionsnightly.txt and versions17.txt ..."
PHP_VERSION=("7.1-apache" "7.2-apache" "7.3-apache" "7.1-fpm" "7.2-fpm" "7.3-fpm")
MAJOR_VERSION=("17" "nightly")
for php_version in ${PHP_VERSION[@]}; do
    for major_version in ${MAJOR_VERSION[@]}; do
        version=$(grep "." "versions${major_version}.txt" | tail -1)
        generate_image $php_version $version
    done
done
