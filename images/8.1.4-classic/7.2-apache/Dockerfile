FROM prestashop/base:7.2-apache
LABEL maintainer="PrestaShop Core Team <coreteam@prestashop.com>"

ENV PS_VERSION=8.1.4

# Get PrestaShop
ADD https://github.com/PrestaShopCorp/prestashop-classic/releases/download/classic-v1.1.36/prestashop_8.1.4.zip /tmp/prestashop.zip

# Extract
RUN mkdir -p /tmp/data-ps \
	&& unzip -q /tmp/prestashop.zip -d /tmp/data-ps/ \
	&& bash /tmp/ps-extractor.sh /tmp/data-ps \
	&& rm /tmp/prestashop.zip
