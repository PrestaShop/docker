#!/bin/sh

BASEDIR=$(dirname "$0")

$BASEDIR/install-environment.sh

echo Generate PrestaShop docker base files
cd $BASEDIR/..
python3 prestashop_docker.py generate
