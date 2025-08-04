FROM prestashop/base:7.2-fpm
LABEL maintainer="PrestaShop Core Team <coreteam@prestashop.com>"

ENV PS_VERSION=1.7.8.1

# Get PrestaShop
ADD https://api.prestashop-project.org/assets/prestashop/1.7.8.1/prestashop.zip /tmp/prestashop.zip

# Extract
RUN mkdir -p /tmp/data-ps \
	&& unzip -q /tmp/prestashop.zip -d /tmp/data-ps/ \
	&& bash /tmp/ps-extractor.sh /tmp/data-ps \
	&& rm /tmp/prestashop.zip
