FROM google/cloud-sdk:latest as nightly-storage

RUN gsutil cp `gsutil ls gs://prestashop-core-nightly/ | grep -E 'develop.+\.zip$' | tail -1` /tmp/prestashop.zip


FROM prestashop/base:7.2-fpm
LABEL maintainer="Thomas Nabord <thomas.nabord@prestashop.com>"

ENV PS_VERSION nightly

COPY --from=nightly-storage /tmp/prestashop.zip /tmp/prestashop.zip

# Extract
RUN mkdir -p /tmp/data-ps \
	&& unzip -q /tmp/prestashop.zip -d /tmp/data-ps/ \
	&& bash /tmp/ps-extractor.sh /tmp/data-ps \
	&& rm /tmp/prestashop.zip
