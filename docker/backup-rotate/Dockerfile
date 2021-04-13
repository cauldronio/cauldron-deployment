FROM python:3.8
LABEL maintainer="contact@cauldron.io"

ENV PYTHONBUFFERED 1

WORKDIR /

RUN apt-get update \
    && apt-get install --no-install-recommends -y cron nano mariadb-client\
    && rm -rf /var/lib/apt/lists/*

ADD requirements.txt /
ADD cron_files /cron_files
ADD entrypoint.sh /

RUN chmod 755 /cron_files/*
RUN chmod 755 /entrypoint.sh

RUN mkdir /snapshots
RUN mkdir /mysqldump

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["/entrypoint.sh"]
