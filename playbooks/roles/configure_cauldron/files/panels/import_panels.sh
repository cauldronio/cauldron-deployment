#!/bin/bash

if [ "$#" -ne 4 ]; then
    echo "USAGE: ${0} <KIDASH_PATH> <ES_URL> <INDEX> <JSON_DIR>"
    exit 1
fi

KIDASH=$1
ES_URL=$2
INDEX=$3
JSON_DIR=$4

for JSON_FILE in ${JSON_DIR}/*.json;
do
  if [[ "${JSON_FILE}" == *config.json ]]; then
    echo "Skipping ${JSON_FILE}"
    continue
  fi
  echo "Importing ${JSON_FILE}"
  ${KIDASH} -e ${ES_URL} --kibana ${INDEX} --import $JSON_FILE
done

echo "...[This is the end]..."
