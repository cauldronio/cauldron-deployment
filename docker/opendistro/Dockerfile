ARG ODFE_VERSION

FROM amazon/opendistro-for-elasticsearch:$ODFE_VERSION

RUN /usr/share/elasticsearch/bin/elasticsearch-plugin install --batch repository-s3
