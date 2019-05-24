#!/bin/bash


# Start MariaDB
echo "Starting MariaDB"
sudo /etc/init.d/mysql start
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start MariaDB: $status"
  exit $status
fi

echo "Waiting for MariaDB to start..."
sudo netstat -cvulntp |grep -m 1 ".*:3306.*LISTEN.*"
echo "MariaDB started"

# Hack from https://github.com/docker-library/mariadb/blob/master/docker-entrypoint.sh
echo "Running files from /docker-entrypoint-initdb.d/"
for f in /docker-entrypoint-initdb.d/*; do
    case "$f" in
        *.sh)     echo "$0: running $f"; . "$f" ;;
        *.sql)    echo "$0: running $f"; mysql < "$f"; echo ;;
        *.sql.gz) echo "$0: running $f"; gunzip -c "$f" | mysql; echo ;;
        *)        echo "$0: ignoring $f" ;;
    esac
    echo
done

sleep 5000d