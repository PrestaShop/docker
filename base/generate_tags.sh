#!/bin/bash

cd $(cd "$( dirname "$0" )" && pwd)

if [ -z "$1" ] || [ "$1" == "-f" ]; then
    PS_VERSIONS_FILE="tags.txt";
else
    PS_VERSIONS_FILE="$1";
fi

while getopts ":f" option; do
   case $option in
      f)
         FORCE=true
         ;;
   esac
done

generate_image()
{
    echo "Generate Dockerfile for PHP $version"

    local version=$1
    local folder="${version}";
    local exec="apache2-foreground";

    if [[ $version = *"fpm"* ]]; then
      exec='php-fpm'
    fi


    if [ -d images/$folder ] && [ -z "$FORCE" ]; then
        # Do not erase what we already defined in the directory
        echo Already defined, skipping Use -f to force update
        return
    fi

    mkdir -p images/$folder/

    sed '
            s/{PHP_TAG}/'"${version}"'/
        ' Dockerfile.model > images/$folder/Dockerfile

    if [[ $version = *"7.1"* || $version = *"7.2"* || $version = *"7.3"* ]]; then
        local before='RUN docker-php-ext-configure gd --with-freetype=\/usr\/include\/ --with-jpeg=\/usr\/include\/ --with-webp=\/usr\/include'
        local after='# PHP < 7.4 have an old syntax to install GD. See https:\/\/github.com\/docker-library\/php\/issues\/912\nRUN docker-php-ext-configure gd --with-freetype-dir=\/usr\/include\/ --with-jpeg-dir=\/usr\/include\/ --with-webp-dir=\/usr\/include'

        sed -i '
            s/'"${before}"'/'"${after}"'/
        ' images/$folder/Dockerfile
    fi
    if [[ $version = *"8.1"* || $version = *"8.2"* || $version = *"8.3"*  || $version = *"8.4"*  || $version = *"8.5"* ]]; then
        local before="FROM php:${version}"
        local after="# Debian Trixie provides a package of the MySQL client that prevent the connexion to succeed for SSL reasons\n# We stick to Bookworm until we find the solution\nFROM php:${version}-bookworm"
        sed -i '
            s/'"${before}"'/'"${after}"'/
        ' images/$folder/Dockerfile
    
        if [[ $version = *"8.5"* ]]; then
            ## -z is used for final line break
            local before='    && if \[ -d \"\/usr\/src\/php\/ext\/opcache\" \]; then docker-php-ext-install opcache; fi \\\n'
            sed -z -i '
                s/'"${before}"'/'""'/g
            ' images/$folder/Dockerfile
        fi
    fi

    cp -R config_files images/$folder/
    sed '
            s/{PHP_CMD}/'"${exec}"'/
        ' config_files/docker_run.sh > images/$folder/config_files/docker_run.sh
}


# Generate base images for PHP tags
echo "Reading tags in ${PS_VERSIONS_FILE} ..."
while read version; do
    generate_image $version
done < $PS_VERSIONS_FILE
