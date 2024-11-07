#!/bin/sh

PS_VERSION=nigthly
PHP_VERSION=8.3
SERVER=apache

if [ $# -gt 0 ]; then
  PS_VERSION=$1
fi
if [ $# -gt 1 ]; then
  PHP_VERSION=$2
fi
if [ $# -gt 2 ]; then
  SERVER=$3
fi

echo Building PrestaShop $PS_VERSION with PHP $PHP_VERSION and Server $SERVER

echo Building base image for PHP $PHP_VERSION with $SERVER
docker build base/images/$PHP_VERSION-$SERVER -t prestashop/base:$PHP_VERSION-$SERVER

echo Building PrestaShop image for version $PS_VERSION
docker build images/$PS_VERSION/$PHP_VERSION-$SERVER -t prestashop/prestashop:$PS_VERSION-$PHP_VERSION-$SERVER

echo Launching docker container with docker compose
PS_VERSION=$PS_VERSION PHP_VERSION=$PHP_VERSION SERVER=$SERVER docker compose -f images/docker-compose.yml up
