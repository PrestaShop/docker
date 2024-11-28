FROM prestashop/base:7.3-fpm
LABEL maintainer="PrestaShop Core Team <coreteam@prestashop.com>"

RUN apt update
RUN apt -y install git

ENV PS_BRANCH=8.1.x
ENV NODE_VERSION=v16.20.2

CMD ["/tmp/docker_branch_run.sh"]
