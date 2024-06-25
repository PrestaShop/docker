#!/bin/bash

BASEDIR=$(dirname "$0")

echo Install python and pip
apt update
apt-get install -y python3-pip

cd $BASEDIR/..
requirements=`cat requirements.txt`
for requirement in $requirements; do
  echo Install $requirement
  pip3 install $requirement --break-system-packages
done
