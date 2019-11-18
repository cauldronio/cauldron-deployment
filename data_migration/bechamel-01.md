14th November 2019


## Changes in this version
Public dashboards are included


## Configuration variables

#### Images
```
DB_IMAGE_NAME: "cauldron2/database:0.1.1"
WEB_IMAGE_NAME: "cauldron2/webserver:0.1.3"
WORKER_IMAGE_NAME: "cauldron2/worker:0.1.1"
ELASTIC_IMAGE_NAME: "amazon/opendistro-for-elasticsearch:0.9.0"
KIBANA_IMAGE_NAME: "amazon/opendistro-for-elasticsearch-kibana:0.9.0"
PANELS_IMAGE_NAME: "cauldron2/panels:0.1.2"
```
#### Variables added
None

#### Variables deleted
```
PANELS_PASSWORD: "test-password"
```

## Migration
Run from `cauldron-deployment/playbooks`:
```
ansible-playbook -i inventories/<name> rm_containers.yml
ansible-playbook -i inventories/<name> cauldron.yml --skip-tags worker
```

Wait for all the containers ready
```
docker logs -f elastic_service 
# Wait until is stable. If "Not yet initialized (you may need to run securityadmin)" appears, wait.
docker logs -f cauldron_service 
# Wait until "Start the Cauldron server"
```

Copy bechamel-01-migrations.yml inside the container (Maybe scp the file is needed or wget from gitlab):
```
docker cp bechamel-01-migrations.py cauldron_service:/code/Cauldron2/bechamel-01-migrations.py
docker exec cauldron_service python Cauldron2/bechamel-01-migrations.py
```

```
ansible-playbook -i inventories/<name> cauldron.yml -t worker
```
