FROM prestashop/base:8.3-apache
LABEL maintainer="PrestaShop Core Team <coreteam@prestashop.com>"

RUN apt update
RUN apt -y install git

ENV PS_BRANCH=9.0.x

CMD ["/tmp/docker_branch_run.sh"]
