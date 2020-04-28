FROM python:3.8
MAINTAINER Cauldron team <contact@cauldron.io>

ENV PYTHONBUFFERED 1

ADD kibana_objects /kibana_objects
ADD requirements.txt /requirements.txt
ADD mappings /mappings
ADD configure_opendistro.py /configure_opendistro.py
ADD settings.py /settings.py
ADD aliases.json /aliases.json

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "/configure_opendistro.py"]
