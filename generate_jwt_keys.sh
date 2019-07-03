ssh-keygen -q -t rsa -b 4096 -f jwtR256.key -N "" -C "" -m pem
openssl rsa -in jwtR256.key -pubout -out jwtR256.key.pub.tmp
sed '1d' jwtR256.key.pub.tmp | sed '$d' | sed ':a;N;$!ba;s/\n/ /g' > jwtR256.key.pub
rm jwtR256.key.pub.tmp