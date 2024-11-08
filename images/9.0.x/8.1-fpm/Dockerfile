FROM prestashop/base:8.1-fpm
LABEL maintainer="PrestaShop Core Team <coreteam@prestashop.com>"

RUN apt update
RUN apt -y install git

ENV PS_BRANCH=9.0.x
ENV NODE_VERSION=v20.17.0

CMD ["/tmp/docker_branch_run.sh"]
