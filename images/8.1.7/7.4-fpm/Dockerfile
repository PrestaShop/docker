FROM prestashop/base:7.4-fpm
LABEL maintainer="PrestaShop Core Team <coreteam@prestashop.com>"

ENV PS_VERSION 8.1.7

# Get PrestaShop
ADD https://github.com/PrestaShop/PrestaShop/releases/download/8.1.7/prestashop_8.1.7.zip /tmp/prestashop.zip

# Extract
RUN mkdir -p /tmp/data-ps \
	&& unzip -q /tmp/prestashop.zip -d /tmp/data-ps/ \
	&& bash /tmp/ps-extractor.sh /tmp/data-ps \
	&& rm /tmp/prestashop.zip
