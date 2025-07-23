#!/bin/bash

: ${PLATFORM_ARGS:="linux/arm/v7,linux/arm64/v8,linux/amd64"}
: ${DOCKER_REPOSITORY:="prestashop/base"}

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
    curl --silent -f -lSL https://hub.docker.com/v2/repositories/$1/tags/$2 > /dev/null 2>&1
}

docker_image()
{
    if ! $FORCE && docker_tag_exists ${DOCKER_REPOSITORY} ${version}; then
        echo "Docker Image already pushed : $DOCKER_REPOSITORY:$version"
        return
    else 
        echo "Docker build & tag : $DOCKER_REPOSITORY:$version"
        docker buildx build \
            --progress=plain \
            --platform ${PLATFORM_ARGS} \
            --builder container \
            --tag ${DOCKER_REPOSITORY}:${version} \
            $([ "${PUSH}" == "true" ] && echo "--push" || echo "") \
            images/${version}
    fi
}


# Generate base images for PHP tags
echo "Reading tags in ${PS_VERSIONS_FILE} ..."
while read version; do
    docker_image $version
done < $PS_VERSIONS_FILE
