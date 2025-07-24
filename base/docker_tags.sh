#!/bin/bash

: ${PLATFORM_ARGS:="linux/arm/v7,linux/arm64/v8,linux/amd64"}
: ${DOCKER_REPOSITORY:="prestashop/base"}

cd $(cd "$( dirname "$0" )" && pwd)

# Default values
PS_VERSIONS_FILE="tags.txt"
SINGLE_VERSION=""
FORCE=false
PUSH=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --version)
            SINGLE_VERSION="$2"
            shift 2
            ;;
        --file)
            PS_VERSIONS_FILE="$2"
            shift 2
            ;;
        -f)
            FORCE=true
            shift
            ;;
        -p)
            PUSH=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--version <version>] [--file <filename>] [-f] [-p]"
            exit 1
            ;;
    esac
done

docker_tag_exists() {
    curl --silent -f -lSL https://hub.docker.com/v2/repositories/$1/tags/$2 > /dev/null 2>&1
}

docker_image() {
    version="$1"
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
            $([ "$PUSH" == "true" ] && echo "--push") \
            images/${version}
    fi
}

if [ -n "$SINGLE_VERSION" ]; then
    echo "Building single version: $SINGLE_VERSION"
    docker_image "$SINGLE_VERSION"
else
    echo "Reading tags in ${PS_VERSIONS_FILE} ..."
    while read -r version; do
        [ -z "$version" ] && continue
        docker_image "$version"
    done < "$PS_VERSIONS_FILE"
fi
