#!/bin/bash

cd $(cd "$( dirname "$0" )" && pwd)

if [ -z "$1" ] || [ "$1" == "-p" ]; then
    PS_VERSIONS_FILE="tags.txt";
else
    PS_VERSIONS_FILE="$1";
fi

while getopts ":p" option; do
   case $option in
      p)
         PUSH=true
         ;;
   esac
done

docker_image()
{
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

}


# Generate base images for PHP tags
echo "Reading tags in ${PS_VERSIONS_FILE} ..."
while read version; do
    docker_image $version
done < $PS_VERSIONS_FILE
