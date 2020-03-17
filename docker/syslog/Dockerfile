FROM balabit/syslog-ng:3.24.1

MAINTAINER Cauldron <contact@cauldron.io>

ADD syslog-ng.conf /etc/syslog-ng/syslog-ng.conf

# RUN wget https://raw.githubusercontent.com/matomo-org/matomo-log-analytics/3.x-dev/import_logs.py

# ADD matomo.sh

ENTRYPOINT ["/usr/sbin/syslog-ng", "-F", "--no-caps"]
