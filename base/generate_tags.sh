#!/bin/bash

generate_image()
{
    echo "Generate Dockerfile for PHP $version"

    folder="$version";
    exec="apache2-foreground";
    if [[ $version = *"fpm"* ]]; then
      exec='php-fpm'
    fi


    mkdir -p images/$folder/

    sed  '
            s/{PHP_TAG}/'"$version"'/
        ' Dockerfile.model > images/$folder/Dockerfile

    cp -R config_files/ images/$folder/
    sed  '
            s/{PHP_CMD}/'"$exec"'/
        ' config_files/docker_run.sh > images/$folder/config_files/docker_run.sh
}

if [ -z "$1" ]; then
    ps_versions_file="tags.txt";
else
    ps_versions_file="$1";
fi

# Generate base images for PHP tags
echo "Reading tags in $ps_versions_file ..."
while read version; do
    generate_image
done <$ps_versions_file
