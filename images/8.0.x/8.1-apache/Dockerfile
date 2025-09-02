FROM --platform=linux/amd64 gcr.io/google.com/cloudsdktool/google-cloud-cli:alpine AS gcloud_amd64
FROM --platform=linux/arm64 gcr.io/google.com/cloudsdktool/google-cloud-cli:alpine AS gcloud_arm64
# Google does not provide images for armv7, we use another platform for this case
FROM --platform=linux/amd64 gcr.io/google.com/cloudsdktool/google-cloud-cli:alpine AS gcloud_arm
FROM gcloud_${TARGETARCH} AS gcloud

ENV PS_VERSION=8.0.x

RUN gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true && \
    gcloud config set metrics/environment github_docker_image && \
    gcloud --version

RUN gsutil cp `gsutil ls gs://prestashop-core-nightly/ | grep -E "$PS_VERSION.+\.zip$" | tail -1` /tmp/prestashop.zip

FROM prestashop/base:8.1-apache
LABEL maintainer="PrestaShop Core Team <coreteam@prestashop.com>"

ENV PS_VERSION=8.0.x
COPY --from=gcloud /tmp/prestashop.zip /tmp/prestashop.zip

# Extract PrestaShop files
RUN mkdir -p /tmp/data-ps && \
    unzip -q /tmp/prestashop.zip -d /tmp/data-ps/ && \
    bash /tmp/ps-extractor.sh /tmp/data-ps && \
    rm /tmp/prestashop.zip
