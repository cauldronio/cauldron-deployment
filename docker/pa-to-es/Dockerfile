FROM python:3.8
MAINTAINER Cauldron team <contact@cauldron.io>

ENV PYTHONBUFFERED 1

RUN git clone --depth=1 https://gitlab.com/cauldronio/pa-to-es.git
RUN pip install -r pa-to-es/requirements.txt

COPY ./entrypoint.sh /
RUN chmod 755 /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
