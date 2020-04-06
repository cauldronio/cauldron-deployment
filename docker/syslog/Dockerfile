FROM balabit/syslog-ng:3.24.1

MAINTAINER Cauldron <contact@cauldron.io>

ADD syslog-ng.conf /etc/syslog-ng/syslog-ng.conf

# Add Matomo
RUN apt update
RUN apt install python -y

WORKDIR /log-analytics/

RUN wget https://raw.githubusercontent.com/matomo-org/matomo-log-analytics/3.x-dev/import_logs.py
ADD matomo.sh /log-analytics/matomo.sh
RUN chmod 755 /log-analytics/matomo.sh
RUN chmod 755 /log-analytics/import_logs.py

ENTRYPOINT ["/usr/sbin/syslog-ng", "-F", "--no-caps", "-edv"]
