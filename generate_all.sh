#!/bin/sh

while read version; do
    echo "Generate PrestaShop $version"

    sed -ri '
			s/^{PS_VERSION} .*/\1 '"$version"'/;
			s/^{PS_URL} .*/\1 '"https://www.prestashop.com/download/old/prestashop_$version.zip"'/
		images/$version/Dockerfile' "Dockerfile.model"
done <versions.txt
