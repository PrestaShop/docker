FROM prestashop/base:{PHP_VERSION}
LABEL maintainer="Thomas Nabord <thomas.nabord@prestashop.com>"

ENV PS_VERSION {PS_VERSION}

# Get PrestaShop
ADD {PS_URL} /tmp/prestashop.zip

# Extract
RUN mkdir -p /tmp/data-ps \
	&& unzip -q /tmp/prestashop.zip -d /tmp/data-ps/ \
	&& bash /tmp/ps-extractor.sh /tmp/data-ps \
	&& rm /tmp/prestashop.zip
