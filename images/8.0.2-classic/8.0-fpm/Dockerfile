FROM prestashop/base:8.0-fpm
LABEL maintainer="PrestaShop Core Team <coreteam@prestashop.com>"

ENV PS_VERSION 8.0.2

# Get PrestaShop
ADD https://github.com/PrestaShopCorp/prestashop-classic/releases/download/classic-v1.1.23/prestashop_8.0.2.zip /tmp/prestashop.zip

# Extract
RUN mkdir -p /tmp/data-ps \
	&& unzip -q /tmp/prestashop.zip -d /tmp/data-ps/ \
	&& bash /tmp/ps-extractor.sh /tmp/data-ps \
	&& rm /tmp/prestashop.zip
