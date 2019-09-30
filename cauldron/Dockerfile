FROM python:3.6
MAINTAINER Jose J Merchante <jjmerchante@bitergia.com>

ENV PYTHONBUFFERED 1
ENV CODE_DIR /code
ENV WEB_DIR ${CODE_DIR}/cauldron-web

WORKDIR ${CODE_DIR}

RUN apt-get update && apt-get install -y default-mysql-client

# Download Cauldron code
RUN git clone https://gitlab.com/cauldron2/cauldron-web.git --depth 1

# Add and install requirements
WORKDIR ${WEB_DIR}
RUN pip install -q -r requirements.txt

ADD entrypoint.sh /entrypoint.sh

RUN chmod 755 /entrypoint.sh

EXPOSE 8000

# Volume for dashboards logs
VOLUME ["/dashboard_logs"]

# Entrypoint
ENTRYPOINT ["/entrypoint.sh"]
