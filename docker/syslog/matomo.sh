#!/bin/bash

/log-analytics/import_logs.py \
 --url=$MATOMO_URL/ \
 --idsite=1 --recorders=1 --enable-http-errors --enable-http-redirects --enable-static --enable-bots \
 --login=$MATOMO_USER --password=$MATOMO_PASSWORD --log-format-name=common --recorder-max-payload-size=50 - &>> /log-analytics/matomo.log