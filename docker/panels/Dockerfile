FROM python:3.6
MAINTAINER Jose J Merchante <jjmerchante@bitergia.com>

ENV PYTHONBUFFERED 1

ADD archimedes_panels /panels
ADD requirements.txt /requirements.txt
ADD mappings /mappings
ADD create_defaults_panels.py /exec.py
# Overwrite settings.py with docker run -v your_file.py:/settings.py
ADD settings.py /settings.py

RUN pip install -r requirements.txt


ENTRYPOINT ["python3", "exec.py"]
