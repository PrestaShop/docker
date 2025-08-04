FROM prestashop/base:8.1-apache
LABEL maintainer="PrestaShop Core Team <coreteam@prestashop.com>"

ENV PS_VERSION=9.0.0-1.0-classic

# Get PrestaShop
ADD https://api.prestashop-project.org/assets/prestashop-classic/9.0.0-1.0/prestashop.zip /tmp/prestashop.zip

# Extract
RUN mkdir -p /tmp/data-ps \
	&& unzip -q /tmp/prestashop.zip -d /tmp/data-ps/ \
	&& bash /tmp/ps-extractor.sh /tmp/data-ps \
	&& rm /tmp/prestashop.zip
