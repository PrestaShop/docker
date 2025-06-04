FROM prestashop/base:8.2-fpm
LABEL maintainer="PrestaShop Core Team <coreteam@prestashop.com>"

ENV PS_VERSION 9.0.0-1.0-beta.1-classic

# Get PrestaShop
ADD https://github.com/PrestaShopCorp/prestashop-classic/releases/download/9.0.0-1.0-beta.1/prestashop_9.0.0-1.0-beta.1.zip /tmp/prestashop.zip

# Extract
RUN mkdir -p /tmp/data-ps \
	&& unzip -q /tmp/prestashop.zip -d /tmp/data-ps/ \
	&& bash /tmp/ps-extractor.sh /tmp/data-ps \
	&& rm /tmp/prestashop.zip
