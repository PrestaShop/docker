FROM prestashop/base:7.2-apache
LABEL maintainer="PrestaShop Core Team <coreteam@prestashop.com>"

RUN apt update
RUN apt -y install git

ENV PS_BRANCH=1.7.8.x
ENV NODE_VERSION=v14.20.0

CMD ["/tmp/docker_branch_run.sh"]
