#!/bin/sh

# PrestaShop 1.6
docker tag -f quetzacoalt/prestashop:1.6.1.0 quetzacoalt/prestashop:1.6.1
docker tag -f quetzacoalt/prestashop:1.6.1.0 quetzacoalt/prestashop:1.6
docker tag -f quetzacoalt/prestashop:1.6.1.0 quetzacoalt/prestashop:latest

docker tag -f quetzacoalt/prestashop:1.6.0.14 quetzacoalt/prestashop:1.6.0

# PrestaShop 1.5
docker tag -f quetzacoalt/prestashop:1.5.6.3 quetzacoalt/prestashop:1.5

#PrestaShop 1.4
docker tag -f quetzacoalt/prestashop:1.4.11.1 quetzacoalt/prestashop:1.4

docker push quetzacoalt/prestashop:1.4
docker push quetzacoalt/prestashop:1.5
docker push quetzacoalt/prestashop:1.6
docker push quetzacoalt/prestashop:1.6.0
docker push quetzacoalt/prestashop:1.6.1
docker push quetzacoalt/prestashop:latest
