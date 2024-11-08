#!/bin/sh

PS_VERSION=nigthly
PHP_VERSION=8.3
SERVER=apache

LAUNCH=false
while getopts "lv:p:s:" option; do
   case $option in
      v)
        PS_VERSION=$OPTARG
        ;;
      p)
        PHP_VERSION=$OPTARG
        ;;
      s)
        SERVER=$OPTARG
        ;;
      l)
        LAUNCH=true
        ;;
      :)
        echo "Option $OPTARG requires an argument"
        exit 1
        ;;
      \?)
        echo "$option : invalid option"
        exit 1
        ;;
   esac
done

echo Building PrestaShop $PS_VERSION with PHP $PHP_VERSION and Server $SERVER

echo Building base image for PHP $PHP_VERSION with $SERVER
docker build base/images/$PHP_VERSION-$SERVER -t prestashop/base:$PHP_VERSION-$SERVER

echo Building PrestaShop image for version $PS_VERSION
docker build images/$PS_VERSION/$PHP_VERSION-$SERVER -t prestashop/prestashop:$PS_VERSION-$PHP_VERSION-$SERVER

if [ $LAUNCH == 'true' ]; then
  echo Launching docker container with docker compose
  PS_VERSION=$PS_VERSION PHP_VERSION=$PHP_VERSION SERVER=$SERVER docker compose -f images/docker-compose.yml up
fi
