FROM prestashop/base:7.2-fpm
LABEL maintainer="PrestaShop Core Team <coreteam@prestashop.com>"

ENV PS_VERSION=8.0.x

ENV PATH /root/google-cloud-sdk/bin/:$PATH

RUN apt update
RUN apt -y install \
 python3 \
 curl \
 bash

RUN curl -sSL https://sdk.cloud.google.com | bash
RUN gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true && \
    gcloud config set metrics/environment github_docker_image && \
    gcloud --version

CMD ["/tmp/docker_nightly_run.sh"]
