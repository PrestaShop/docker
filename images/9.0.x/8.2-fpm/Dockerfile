FROM prestashop/base:8.2-fpm
LABEL maintainer="PrestaShop Core Team <coreteam@prestashop.com>"

RUN apt update
RUN apt -y install git

RUN git clone -b 9.0.x https://github.com/PrestaShop/PrestaShop.git /tmp/data-ps

CMD ["/tmp/docker_run.sh"]
