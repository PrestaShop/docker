FROM prestashop/base:7.0-fpm
LABEL maintainer="Thomas Nabord <thomas.nabord@prestashop.com>"

ENV PS_VERSION 1.5.6.3

# Get PrestaShop
ADD https://www.prestashop.com/download/old/prestashop_1.5.6.3.zip /tmp/prestashop.zip

# Extract
RUN mkdir -p /tmp/data-ps \
	&& unzip -q /tmp/prestashop.zip -d /tmp/data-ps/ \
	&& bash /tmp/ps-extractor.sh /tmp/data-ps \
	&& rm /tmp/prestashop.zip
