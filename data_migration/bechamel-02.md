27th November 2019


## Changes in this version
Migrate from Opendistro 0.9.0 to 1.2.0


## Configuration variables

#### Images
```
DB_IMAGE_NAME: "cauldronio/database:0.1.1"
WEB_IMAGE_NAME: "cauldronio/webserver:0.1.5"
WORKER_IMAGE_NAME: "cauldronio/worker:0.1.3"
ELASTIC_IMAGE_NAME: "amazon/opendistro-for-elasticsearch:1.2.0"
KIBANA_IMAGE_NAME: "amazon/opendistro-for-elasticsearch-kibana:1.2.0"
PANELS_IMAGE_NAME: "cauldronio/panels:0.1.4"
```

#### Commits
```
cauldronio/cauldron-worker: "cee8b1fa0432ed9ab89e9538e8bb6ec8adeed421"
cauldronio/cauldron-deployment: "baa856fdb3cdcf4821e8d496733edad1ec282906"
cauldronio/cauldron-web: "091a15b7bbcd6d9a659b4724825912978535dfbf"
```


## Migration
Get a backup of the Opendistro security index:
```
docker exec elastic_service mkdir /backup-elastic6
docker exec elastic_service chmod +x plugins/opendistro_security/tools/securityadmin.sh
docker exec elastic_service plugins/opendistro_security/tools/securityadmin.sh -r -cd /backup-elastic6 -icl -nhnv -cacert config/root-ca.pem -cert config/admin.pem -key config/admin-key.pem
docker cp elastic_service:/backup-elastic6 .
```

Run from `cauldron-deployment/playbooks`:
```
ansible-playbook -i inventories/<name> rm_containers.yml
ansible-playbook -i inventories/<name> cauldron.yml --skip-tags worker,panels,webserver

```

Wait for the containers ready
```
docker logs -f elastic_service
# Wait until is stable. If "Not yet initialized (you may need to run securityadmin)" appears, wait.
docker logs -f kibana_service
# Wait until "Server running at http://0:5601/kibana"
```

Delete the security index and create a new one with the new configuration files
```
docker exec elastic_service chmod +x plugins/opendistro_security/tools/securityadmin.sh
docker exec elastic_service plugins/opendistro_security/tools/securityadmin.sh -dci -icl -nhnv -cacert config/root-ca.pem -cert config/admin.pem -key config/admin-key.pem
docker exec elastic_service plugins/opendistro_security/tools/securityadmin.sh -cd plugins/opendistro_security/securityconfig/ -cacert config/root-ca.pem -cert config/admin.pem -key config/admin-key.pem -icl -nhnv
```

Start Django
```
ansible-playbook -i inventories/<name> cauldron.yml -t webserver
```

Copy bechamel-02-odfe-migrations.py inside the container (Maybe scp the file is needed or wget from gitlab). Run it:
```
docker cp data_migration/bechamel-02-odfe-migrations.py cauldron_service:/code/Cauldron2/
docker exec cauldron_service python Cauldron2/bechamel-02-odfe-migrations.py
```

Run Cauldron
```
ansible-playbook -i inventories/<name> cauldron.yml
```
