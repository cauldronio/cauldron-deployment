# Ansible Role: configure_cauldron

This playbook makes the initial steps in order to deploy cauldron and its dependencies.

## Actions:

#### Docker_build.yml:
* Build a Docker image.

#### Hash_password.yml:
* Generate hashes for each item in `<loop_psw>` and get result.
* Set variable `<loop_output>` to be equal to the output of the previous task.

#### Configure_workers.yml:
* Create `<configuration_dir>/mordred` directory if not exists.
* Copy the file `worker_config.py.j2` to `<configuration_dir>/mordred/worker_config.py`
* Copy the file `setup-default.cfg.j2` to `<configuration_dir>/mordred/setup-default.cfg`

#### Configure_panels.yml:
* Create `<configuration_dir>/archimedes_panels` directory if not exists.
* Copy the file `panels-config.py.j2` to `<configuration_dir>/archimedes_panels/settings.py`

#### Configure_jwt_keys.yml:
* Create the private key for JWT.
* Create the public key for JWT.
* Prepare the JWT public key for ES.

#### Configure_database.yml:
* Create `<configuration_dir>/database` directory if not exists.
* Copy the file `database.sql.j2` to `<configuration_dir>/database/database.sql`

#### Configure_nginx.yml:
* Create `<configuration_dir>/nginx` directory if not exists.
* Create `<configuration_dir>/nginx/certificates` directory if not exists.
* Copy the file `nginx_cauldron.conf.j2` to `<configuration_dir>/nginx/nginx_cauldron.conf`
* Copy the file `keys/ssl_server.crt` to `<configuration_dir>/nginx/certificates` and set permissions `0644`.
* Copy the file `keys/ssl_server.key` to `<configuration_dir>/nginx/certificates` and set permissions `0644`.

#### Configure_opendistro.yml:
* Create `<configuration_dir>/es` directory if not exists.
* Create `<configuration_dir>/kibana` directory if not exists.
* Copy the directory `keys` to `<configuration_dir>/es/` and set permissions `0644`.
* Copy the file `elasticsearch-secured.yml.j2` to `<configuration_dir>/es/elasticsearch-secured.yml` and set permissions `0644`.
* Copy the file `opendistro-config.yml.j2` to `<configuration_dir>/es/opendistro-config.yml` and set permissions `0644`.
* Copy the file `kibana.yml.j2` to `<configuration_dir>/kibana/kibana.yml` and set permissions `0644`.
* Create hashes for Elasticsearch passwords.
* Copy the file `internal_users.yml.j2` to `<configuration_dir>/es/internal_users.yml` and set permissions `0644`.

#### Docker_build.yml (django):
* Build the Django Docker image `<django_image>` located at `<django_image_location>`.

#### Docker_build.yml (mordred):
* Build the Mordred Docker image `<mordred_image>` located at `<mordred_image_location>`.

#### Docker_build.yml (database):
* Build the Database Docker image `<db_image>` located at `<db_image_location>`.

#### Docker_build.yml (panels):
* Build the Panels Docker image `<panels_image>` located at `<panels_image_location>`.

#### Docker_pull.yml (elasticsearch):
* Pull the ES Docker image `<es_image>` from Docker Hub.

#### Docker_pull.yml (kibana):
* Pull the Kibana Docker image `<kibana_image>` from Docker Hub.

#### Docker_pull.yml (mysql):
* Pull the MySQL Docker image `mysql` from Docker Hub.

#### Docker_pull.yml (nginx):
* Pull the Nginx Docker image `<nginx_image>` from Docker Hub.

#### Create_network.yml:
* Create a Docker network to connect every container, specifying the name of the network with the variable `<network_name>`.

#### Configure_django.yml:
* Create a secret key for Django.
* Create `<configuration_dir>/django` directory if not exists.
* Copy the file `django_settings.py.j2` to `<configuration_dir>/django/django_settings.py`

#### Docker_pull.yml:
* Pull a Docker image from Docker Hub.

#### Create_volume.yml:
* Create a Docker volume for Cauldron, named by var `<volume_name>`.
* Create a Docker volume for Elasticsearch, named by var `<es_volume>`.

## Tags:

* `create_image` - Tasks related with the creation of Docker images.

## Variables:

* `task_image_name` - Name of the Docker image.



* `task_image_location` - Path or URL of the Docker image.



* `passwords_container`: `tmp_container_passwords` - Name of the temporary passwords container.



* `es_image`: `amazon/opendistro-for-elasticsearch:0.9.0` - Name of the ES Docker image.



* `loop_psw` - List of the Open Distro essentials passwords.



* `loop_output` - List of the output hashes.



* `configuration_dir`: `/tmp` - Main configuration directory.



* `es_admin_password`: `ChangeAdminPassword` - Password for the Elasticsearch admin user.



* `es_logstash_password`: `logstash` - Password for Logstash.



* `es_kibanaserver_password`: `kibanaserver` - Password for the Kibana server.



* `es_kibanaro_password`: `kibanaro` - Password for the Kibana root user.



* `es_readall_password`: `readall` - Password for the Read-all Kibana user.



* `es_snapshotrestore_password`: `snapshotrestore` - Password for the Kibana Snapshot and Restore.



* `django_image_location`: `https://gitlab.com/cauldron2/cauldron-deployment.git#:cauldron` - URL of the Django Docker image.



* `django_image`: `cauldron` - Name of the Django Docker image.



* `mordred_image_location`: `https://gitlab.com/cauldron2/cauldron-deployment.git#:mordred` - URL of the Mordred Docker image.



* `mordred_image`: `cauldron` - Name of the Mordred Docker image.



* `db_image_location`: `https://gitlab.com/cauldron2/cauldron-deployment.git#:database` - URL of the Database Docker image.



* `db_image`: `database_cauldron` - Name of the Database Docker image.



* `panels_image_location`: `https://gitlab.com/cauldron2/cauldron-deployment.git#:docker-panels` - URL of the Panels Docker image.



* `panels_image`: `panels_image` - Name of the Panels Docker image.



* `kibana_image`: `amazon/opendistro-for-elasticsearch-kibana:0.9.0` - Name of the Kibana Docker image.



* `nginx_image`: `nginx` - Name of the Nginx Docker image.



* `network_name`: `network_cauldron` - Name of the Docker network used.



* `volume_name`: `cauldron_volume` - Name of the Cauldron volume.



* `es_volume`: `elastic_data` - Name of the Elasticsearch volume.
