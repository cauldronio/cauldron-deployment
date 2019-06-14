#!/usr/bin/env bash
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

# Generate Kibana certificate
openssl genrsa -out kibana-key-temp.pem 2048
openssl pkcs8 -inform PEM -outform PEM -in kibana-key-temp.pem -topk8 -nocrypt -v1 PBE-SHA1-3DES -out kibana-key.pem
openssl req -new -key kibana-key.pem -out kibana.csr -subj "/C=EU/ST=Any/L=All/O=Dis/CN=kibana"
openssl x509 -req -days 3650 -in kibana.csr -CA root-ca.pem -CAkey root-ca-key.pem -CAcreateserial -sha256 -out kibana.pem


# Clean up
rm admin-key-temp.pem
rm admin.csr
rm node-1-key-temp.pem
rm node-1.csr
rm kibana.csr
rm kibana-key-temp.pem

# Show expiration dates
echo ""
echo "Expiration dates:"
openssl x509 -enddate -noout -in root-ca.pem
openssl x509 -enddate -noout -in admin.pem
openssl x509 -enddate -noout -in node-1.pem
openssl x509 -enddate -noout -in kibana.pem
echo ""
echo "Nodes dn:"
echo "Root:"
openssl x509 -subject -nameopt RFC2253 -noout -in root-ca.pem
echo "Admin:"
openssl x509 -subject -nameopt RFC2253 -noout -in admin.pem
echo "Node-1:"
openssl x509 -subject -nameopt RFC2253 -noout -in node-1.pem
echo "kibana:"
openssl x509 -subject -nameopt RFC2253 -noout -in kibana.pem
echo
echo "If you changed any configuration of this file, maybe you have to change something in templates/elasticsearch-secured.yml.j2"