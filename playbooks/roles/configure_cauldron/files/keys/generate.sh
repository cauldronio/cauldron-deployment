#!/usr/bin/env bash

##################################################################################
# IMPORTANT NOTE: If you change the CN in configuration of this file,            #
# maybe you have to change something in templates/elasticsearch-secured.yml.j2   #
##################################################################################


# Generate Root certificate
openssl genrsa -out root-ca-key.pem 2048
openssl req -new -x509 -sha256 -days 3650 -key root-ca-key.pem -out root-ca.pem -subj "/C=EU/ST=Any/L=All/O=Dis/CN=elastic_service"

# Generate Admin certificate
openssl genrsa -out admin-key-temp.pem 2048
openssl pkcs8 -inform PEM -outform PEM -in admin-key-temp.pem -topk8 -nocrypt -v1 PBE-SHA1-3DES -out admin-key.pem
openssl req -new -key admin-key.pem -out admin.csr -subj "/C=EU/ST=Any/L=All/O=Dis/CN=admin"
openssl x509 -req -days 3650 -in admin.csr -CA root-ca.pem -CAkey root-ca-key.pem -CAcreateserial -sha256 -out admin.pem

# Generate Node certificate
openssl genrsa -out node-1-key-temp.pem 2048
openssl pkcs8 -inform PEM -outform PEM -in node-1-key-temp.pem -topk8 -nocrypt -v1 PBE-SHA1-3DES -out node-1-key.pem
openssl req -new -key node-1-key.pem -out node-1.csr -subj "/C=EU/ST=Any/L=All/O=Dis/CN=elastic_service"
openssl x509 -req -days 3650 -in node-1.csr -CA root-ca.pem -CAkey root-ca-key.pem -CAcreateserial -sha256 -out node-1.pem

# Generate Nginx certificate
openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout ssl_server.key -out ssl_server.crt -subj "/C=EU/ST=Any/L=All/O=Dis/CN=selfsigned"

# Clean up
rm admin-key-temp.pem
rm admin.csr
rm node-1-key-temp.pem
rm node-1.csr

# Show expiration dates
echo ""
echo "Expiration dates:"
openssl x509 -enddate -noout -in root-ca.pem
openssl x509 -enddate -noout -in admin.pem
openssl x509 -enddate -noout -in node-1.pem
openssl x509 -enddate -noout -in ssl_server.crt
echo ""
echo "Nodes dn:"
echo "Root:"
openssl x509 -subject -nameopt RFC2253 -noout -in root-ca.pem
echo "Admin:"
openssl x509 -subject -nameopt RFC2253 -noout -in admin.pem
echo "Node-1:"
openssl x509 -subject -nameopt RFC2253 -noout -in node-1.pem
echo "Nginx ssl:"
openssl x509 -subject -nameopt RFC2253 -noout -in ssl_server.crt

echo