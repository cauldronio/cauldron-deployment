#!/usr/bin/env bash

printenv | grep -E "(ODFE_HOST|ODFE_ADMIN_PASSWORD|DB_HOST|DB_PASSWORD)" >> /etc/environment

if [ ! -z "$LOCAL_BACKUP" ]
then
  echo "Enable local backup"
  printenv | grep -E "(ODFE_LOCAL_SNAPSHOT_REPO)" >> /etc/environment
  cp /cron_files/000_create_local_snapshot /etc/cron.daily/
  cp /cron_files/001_create_local_sqldump /etc/cron.daily/
  cp /cron_files/004_remove_local_snapshot /etc/cron.daily/
  cp /cron_files/005_remove_local_sqldump /etc/cron.daily/
fi

if [ ! -z "$S3_BACKUP" ]
then
  if [[ -z $S3_ENDPOINT || -z $S3_BUCKET || -z $S3_PATH || -z $S3_ACCESS_KEY || -z $S3_SECRET_KEY ]]; then
    echo 'S3 enabled but missing configuration'
    exit 1
  fi
  echo "Enable S3 backup"
  printenv | grep -E "(S3_ENDPOINT|S3_BUCKET|S3_PATH|S3_ACCESS_KEY|S3_SECRET_KEY|ODFE_S3_SNAPSHOT_REPO)" >> /etc/environment
  cp /cron_files/002_create_s3_snapshot /etc/cron.daily/
  cp /cron_files/003_create_s3_sqldump /etc/cron.daily/
  cp /cron_files/006_remove_s3_snapshot /etc/cron.daily/
  cp /cron_files/007_remove_s3_sqldump /etc/cron.daily/
fi

if [ -z "$S3_BACKUP" ] &&  [ -z "$LOCAL_BACKUP" ]
then
  echo "Backup not enabled for S3 or Local"
else
  cron -f
fi
