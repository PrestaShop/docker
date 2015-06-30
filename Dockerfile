FROM php:5.6-apache

MAINTAINER Thomas Nabord <thomas.nabord@prestashop.com

ENV DB_SERVER 127.0.0.1
ENV DB_NAME prestashop
ENV DB_USER root
ENV DB_PASSWD admin
ENV ADMIN_MAIL demo@prestashop.com
ENV ADMIN_PASSWD prestashop_demo

# Avoid MySQL questions during installation
ENV DEBIAN_FRONTEND noninteractive
RUN echo mysql-server-5.6 mysql-server/root_password password $DB_PASSWD | debconf-set-selections
RUN echo mysql-server-5.6 mysql-server/root_password_again password $DB_PASSWD | debconf-set-selections

COPY ./extracts/prestashop/ /var/www/html/

RUN apt-get update \
	&& apt-get install -y libmcrypt-dev \
		libjpeg62-turbo-dev \
		libpng12-dev \
		libfreetype6-dev \
		mysql-client \
		mysql-server \
	&& docker-php-ext-install iconv mcrypt pdo mysql pdo_mysql mbstring \
    && docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ \
    && docker-php-ext-install gd

# Apache configuration
RUN a2enmod rewrite
RUN chown www-data:www-data -R /var/www/html/

RUN mv /var/www/html/install /var/www/html/install-dev
RUN mv /var/www/html/admin /var/www/html/admin-dev

# PHP configuration
COPY config/php.ini /usr/local/etc/php5

# MySQL configuration
RUN sed -i -e"s/^bind-address\s*=\s*127.0.0.1/bind-address = 0.0.0.0/" /etc/mysql/my.cnf
EXPOSE 3306

COPY docker_run.sh /tmp/
ENTRYPOINT ["/tmp/docker_run.sh"]
