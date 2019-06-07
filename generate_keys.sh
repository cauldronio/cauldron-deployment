ssh-keygen -q -t rsa -b 4096 -f jwtR256.key -N "" -C "" -m pem
openssl rsa -in jwtR256.key -pubout -out jwtR256.key.pub