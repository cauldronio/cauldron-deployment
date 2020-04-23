#!/usr/bin/env bash

##################################################################################
# IMPORTANT NOTE: If you change the CN in configuration of this file,            #
# maybe you have to change something in templates/elasticsearch-secured.yml.j2   #
##################################################################################

# This files creates (if not exist):
#  - Root certificate for Elasticsearch
#  - Admin certificate for Elasticsearch
#  - One node certificate for Elasticsearch
#  - NGINX ssl keys

INITDIR=`pwd`
ES_KEYS_PATH=es_keys
NGINX_KEYS_PATH=nginx_keys
JWT_KEY_PATH=jwt_key

cd $ES_KEYS_PATH

if [ ! -f root-ca-key.pem ] || [ ! -f root-ca.pem ]; then
    echo "==> Generating root certificate for ElasticSearch"
    openssl genrsa -out root-ca-key.pem 2048
    openssl req -new -x509 -sha256 -days 3650 -key root-ca-key.pem -out root-ca.pem -subj "/C=EU/ST=Any/L=All/O=Dis/CN=elastic_service"
else
    echo "==> Root certificate for ElasticSearch exists ($ES_KEYS_PATH/root-ca*.pem)"
fi
echo

if [ ! -f admin-key.pem ] || [ ! -f admin.pem ]; then
    echo "==> Generating admin certificate for ElasticSearch"
    openssl genrsa -out admin-key-temp.pem 2048
    openssl pkcs8 -inform PEM -outform PEM -in admin-key-temp.pem -topk8 -nocrypt -v1 PBE-SHA1-3DES -out admin-key.pem
    openssl req -new -key admin-key.pem -out admin-temp.csr -subj "/C=EU/ST=Any/L=All/O=Dis/CN=admin"
    openssl x509 -req -days 3650 -in admin-temp.csr -CA root-ca.pem -CAkey root-ca-key.pem -CAcreateserial -sha256 -out admin.pem
    rm admin-key-temp.pem
    rm admin-temp.csr
else
    echo "==> Admin certificate for ElasticSearch exists ($ES_KEYS_PATH/admin*.pem)"
fi
echo

if [ ! -f node-1-key.pem ] || [ ! -f node-1.pem ]; then
    echo "==> Generating one node certificate for ElasticSearch"
    openssl genrsa -out node-1-key-temp.pem 2048
    openssl pkcs8 -inform PEM -outform PEM -in node-1-key-temp.pem -topk8 -nocrypt -v1 PBE-SHA1-3DES -out node-1-key.pem
    openssl req -new -key node-1-key.pem -out node-1-temp.csr -subj "/C=EU/ST=Any/L=All/O=Dis/CN=elastic_service"
    openssl x509 -req -days 3650 -in node-1-temp.csr -CA root-ca.pem -CAkey root-ca-key.pem -CAcreateserial -sha256 -out node-1.pem
    rm node-1-key-temp.pem
    rm node-1-temp.csr
else
    echo "==> Node-1 certificate for ElasticSearch exists ($ES_KEYS_PATH/node-1*.pem)"
fi
echo

cd $INITDIR


cd $NGINX_KEYS_PATH

if [ ! -f ssl_server.key ] || [ ! -f ssl_server.crt ]; then
    echo "==> Generating SSL keys for NGINX"
    openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout ssl_server.key -out ssl_server.crt -subj "/C=EU/ST=Any/L=All/O=Dis/CN=selfsigned"
else
    echo "==> SSL keys for NGINX exists ($NGINX_KEYS_PATH/ssl_server.*)"
fi
echo

cd $INITDIR


cd $JWT_KEY_PATH

if [ ! -f jwtR256.key ] || [ ! -f jwtR256.key.pub ]; then
    echo "==> Generating JWT key pair for Django"
    ssh-keygen -q -t rsa -b 4096 -f jwtR256.key -N '' -C '' -m pem
else
    echo "==> JWT key pair for Django exists ($JWT_KEY_PATH/jwtR256.*)"
fi
echo

if [ ! -f pub.jwtR256.key ]; then
    echo "==> Generating JWT public key for Elastic"
    openssl rsa -in jwtR256.key -pubout -out pub.jwtR256.key
else
    echo "==> JWT public key for Elastic exists ($JWT_KEY_PATH/pub.jwtR256.key)"
fi
echo

cd $INITDIR


# Show expiration dates
echo ""
echo "Expiration dates for the certificates:"
echo -n "root: "
openssl x509 -enddate -noout -in $ES_KEYS_PATH/root-ca.pem
echo -n "admin: "
openssl x509 -enddate -noout -in $ES_KEYS_PATH/admin.pem
echo -n "node-1: "
openssl x509 -enddate -noout -in $ES_KEYS_PATH/node-1.pem
echo -n "ssl_nginx: "
openssl x509 -enddate -noout -in $NGINX_KEYS_PATH/ssl_server.crt
echo
