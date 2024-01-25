#!/bin/bash

cd $(cd "$( dirname "$0" )" && pwd)

if [ -z "$1" ] || [ "$1" == "-p" ]; then
    PS_VERSIONS_FILE="tags.txt";
else
    PS_VERSIONS_FILE="$1";
fi

FORCE=false
while getopts ":fp" option; do
   case $option in
      p)
         PUSH=true
         ;;
      f)
         FORCE=true
         ;;
   esac
done

docker_tag_exists() {
    curl --silent -f -lSL https://hub.docker.com/v2/repositories/$1/tags/$2 > /dev/null
}

docker_image()
{
    if ! $FORCE && docker_tag_exists prestashop/base ${version}; then
        echo "Docker Image already pushed : prestashop/base:$version"
        return
    else 
        echo "Docker build & tag : prestashop/base:$version"
        id=$(echo $(docker build --quiet=true images/${version} 2>/dev/null) | awk '{print $NF}')
        echo $id;
        docker tag $id prestashop/base:${version}


        if [ -z "$PUSH" ]; then
            # Do not push
            return
        fi
        echo "Docker Push : prestashop/base:$version"

        docker push prestashop/base:${version}
    fi
}


# Generate base images for PHP tags
echo "Reading tags in ${PS_VERSIONS_FILE} ..."
while read version; do
    docker_image $version
done < $PS_VERSIONS_FILE
