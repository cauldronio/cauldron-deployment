FROM python:3.6
MAINTAINER Jose J Merchante <jjmerchante@bitergia.com>

ENV PYTHONBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN apt update && apt install -y mysql-client

# Download Cauldron code
RUN git clone https://gitlab.com/cauldron2/cauldron.git --depth 1

# Add and install requirements
WORKDIR /code/cauldron
RUN pip install -q -r requirements.txt

ADD entrypoint.sh /entrypoint.sh
ADD settings_secret.py /code/settings_secret.py

RUN chmod 755 /entrypoint.sh

# Entrypoint
ENTRYPOINT ["/entrypoint.sh"]
