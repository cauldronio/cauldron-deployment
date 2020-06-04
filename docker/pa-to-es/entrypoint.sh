#!/bin/bash

python pa-to-es/main.py \
  --seven \
  -e $ELASTIC_HOST \
  -u admin \
  -p $ELASTIC_PASSWORD
