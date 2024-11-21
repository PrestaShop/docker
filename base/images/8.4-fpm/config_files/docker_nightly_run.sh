#!/bin/sh

# Download nightly build
if [ ! -d /tmp/data-ps ]; then
    gsutil cp `gsutil ls gs://prestashop-core-nightly/ | grep -E 'develop.+\.zip$$' | tail -1` /tmp/prestashop.zip

    mkdir -p /tmp/data-ps
    unzip -q /tmp/prestashop.zip -d /tmp/data-ps/

    bash /tmp/ps-extractor.sh /tmp/data-ps

    # Remove downloaded zip
    rm /tmp/prestashop.zip
fi

/tmp/docker_run.sh
