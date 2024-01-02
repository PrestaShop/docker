FROM prestashop/base:7.2-fpm
LABEL maintainer="PrestaShop Core Team <coreteam@prestashop.com>"

ENV PS_VERSION 1.7.8.11

# Get PrestaShop
ADD https://github.com/PrestaShop/PrestaShop/releases/download/1.7.8.11/prestashop_1.7.8.11.zip /tmp/prestashop.zip

# Extract
RUN mkdir -p /tmp/data-ps \
	&& unzip -q /tmp/prestashop.zip -d /tmp/data-ps/ \
	&& bash /tmp/ps-extractor.sh /tmp/data-ps \
	&& rm /tmp/prestashop.zip
