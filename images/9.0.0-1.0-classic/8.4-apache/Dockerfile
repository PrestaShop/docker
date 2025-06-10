FROM prestashop/base:8.4-apache
LABEL maintainer="PrestaShop Core Team <coreteam@prestashop.com>"

ENV PS_VERSION 9.0.0-1.0-classic

# Get PrestaShop
ADD https://github.com/PrestaShopCorp/prestashop-classic/releases/download/9.0.0-1.0/prestashop_9.0.0-1.0.zip /tmp/prestashop.zip

# Extract
RUN mkdir -p /tmp/data-ps \
	&& unzip -q /tmp/prestashop.zip -d /tmp/data-ps/ \
	&& bash /tmp/ps-extractor.sh /tmp/data-ps \
	&& rm /tmp/prestashop.zip
