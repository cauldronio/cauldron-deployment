FROM debian:stretch-slim

USER root

RUN apt-get update && \
    apt-get -y install --no-install-recommends \
        mariadb-client \
        unzip curl wget sudo ssh \
        net-tools

# Install MariaDB
RUN apt-get -y install --no-install-recommends mariadb-server
RUN echo "mysqld_safe &" > /tmp/config && \
    echo "mysqladmin --silent --wait=30 ping || exit 1" >> /tmp/config && \
    bash /tmp/config && \
    rm -f /tmp/config && \
    sed -e "/bind-address/s/^/#/g" -i /etc/mysql/mariadb.conf.d/50-server.cnf
EXPOSE 3306

RUN mkdir "/docker-entrypoint-initdb.d"

ADD entrypoint.sh /entrypoint.sh
RUN sudo chmod 755 /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]