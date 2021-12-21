FROM amazon/opendistro-for-elasticsearch:1.13.3

WORKDIR /usr/share/elasticsearch

ENV PATH=/usr/share/elasticsearch/bin:$PATH

RUN elasticsearch-plugin install --batch repository-s3

RUN /usr/share/elasticsearch/bin/elasticsearch-keystore create

COPY checksums/log4j /tmp/

RUN cd /usr/local/lib && \
    wget https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-core/2.17.0/log4j-core-2.17.0.jar -O log4j-core.jar && \
    wget https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-api/2.17.0/log4j-api-2.17.0.jar -O log4j-api.jar && \
    wget https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-slf4j-impl/2.17.0/log4j-slf4j-impl-2.17.0.jar -O log4j-slf4j-impl.jar && \
    wget https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-1.2-api/2.17.0/log4j-1.2-api-2.17.0.jar -O log4j-1.2-api.jar && \
    sha1sum -c /tmp/log4j && \
    rm /tmp/log4j

COPY scripts/replace_log4j.sh /tmp/

RUN /tmp/replace_log4j.sh && \
    rm /tmp/replace_log4j.sh
