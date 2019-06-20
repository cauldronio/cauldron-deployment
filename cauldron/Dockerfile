FROM python:3.6
MAINTAINER Jose J Merchante <jjmerchante@bitergia.com>

ENV PYTHONBUFFERED 1

RUN mkdir /logs
RUN mkdir /code
WORKDIR /code

RUN apt-get update && apt-get install -y mysql-client

# Install packages for nginx + django and certificates
RUN apt-get install -y nginx certbot python-certbot-nginx supervisor
RUN pip install gunicorn

ADD start_gunicorn.sh /code/
RUN chmod 777 /code/start_gunicorn.sh

ADD supervisor_cauldron.conf /etc/supervisor/conf.d/

ADD nginx_cauldron.conf /etc/nginx/sites-enabled/

RUN mkdir /etc/nginx/ssl
ADD default_ssl_keys/cert.pem /etc/nginx/ssl/server.crt
ADD default_ssl_keys/key.pem /etc/nginx/ssl/server.key

# Download Cauldron code
RUN git clone https://gitlab.com/cauldron2/cauldron.git --depth 1

# Add and install requirements
WORKDIR /code/cauldron
RUN pip install -q -r requirements.txt

ADD entrypoint.sh /entrypoint.sh

RUN chmod 755 /entrypoint.sh

# Volume for dashboards logs
VOLUME ["/dashboard_logs"]

# Entrypoint
ENTRYPOINT ["/entrypoint.sh"]
