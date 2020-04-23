# Cauldron deployment

This repository contains relevant information for running Cauldron in your own computer or in a remote system.

- [Requirements](#requirements)
- [Preconfiguration](#preconfiguration)
- [Run and stop Cauldron](#run-and-stop-cauldron)
- [Matomo analytics](#matomo-analytics)
- [Advanced deployment for Cauldron](#advanced-deployment-for-cauldron)
- [Development environment](#development-environment)
- [Continuous Delivery and Rolling Upgrades](#continuous-delivery-and-rolling-upgrades)
- [Admin page](#admin-page)
- [Backups](#backups)
- [Troubleshooting](#troubleshooting)

## Requirements

- It's necessary that you have **Ansible** (~2.8) installed in your computer in order to run the playbooks. You can follow [this link](https://docs.ansible.com/ansible/latest/installation_guide/) to find the installation docs.

  **NOTE**: Ansible works by default with your system's default Python version, but the playbooks for Cauldron are prepared for Python 3. Anyway, please check your Ansible configuration to be sure about which Python version is being used by executing:
  ```bash
   $ ansible --version
  ```

- **Terraform** is an ***optional*** requirement in case you want to automate the provisioning of the machine used for the deployment. You have more information about how to carry out this provisioning [here](do/README.md).

- **Docker** (~18.09) is also needed for running the containers. You can install it by following [this link](https://docs.docker.com/install/).

  **IMPORTANT**: You will also need to add your own user to the docker group created during the installation of Docker in order to execute Docker CLI without `sudo`:
  ```bash
   $ sudo usermod -aG docker $USER
  ```

- **Docker SDK for Python** is required by Ansible to execute Docker commands in Python scripts. For Python 3 you will need to execute the following:
  ```bash
    $ pip3 install docker
  ```

- **virtualenv** is necessary for creating a Python environment for generating the hashed keys for OpenDistro for ElasticSearch:
  ``` bash
    $ virtualenv --version
  ```

- **rsync** is necessary for copying the files to a remote machine. To check if you have it installed:
  ``` bash
    $ rsync --version
  ```

- The following ports will be used in the target machine. You can change this later in the configuration file.

  - **9000**: Cauldron web interface


## Preconfiguration

### Clone the latest version of this repository:
```bash
$ git clone https://gitlab.com/cauldronio/cauldron-deployment.git
$ cd cauldron-deployment
```

### Create Oauth application keys for each backend or the those that you want to use:

<details>
<summary>GitHub</summary>

- Create a [GitHub Oauth App](https://developer.github.com/apps/building-oauth-apps/creating-an-oauth-app/). After the registration, you can obtain the `Client ID` and `Client Secret`:
    - **Application name**: A name for the application, for example `Bitergia Cauldron`
    - **Homepage URL**: This should be the full URL to your application homepage. If you will run it in your local computer, you can type `https://localhost:9000/`. (You can change it later)
    - **Application description**: Not required
    - **Authorization callback URL**: This is important. It should be the Homepage URL and `/github-login`. For example, for your local computer: `https://localhost:9000/github-login`. (You can change it later)

</details>


<details>
<summary>GitLab</summary>

- Create a [Gitlab Oauth App](https://docs.gitlab.com/ee/integration/oauth_provider.html#adding-an-application-through-the-profile). After the registration, you can obtain the `Application ID` and `Secret`.:
    - **Name**: A name for the application, for example `Bitergia Cauldron`
    - **Redirect URI**: This is important. It should be the Homepage URL and `/gitlab-login`. For example, for your local computer: `https://localhost:9000/gitlab-login`. (You can change it later)
    - **Scopes**: Select only `api`

</details>


<details>
<summary>Meetup</summary>

**Important**: Meetup API has changed and you cannot create free applications anymore. We keep this section if you have a Meetup Pro account.

- Create a [Meetup Oauth App](https://secure.meetup.com/meetup_api/oauth_consumers/create/). After the registration, you can obtain the `Application ID` and `Secret`:
    - **Consumer Name**: A name for the application, for example `Bitergia Cauldron`
    - **Application website**: A website for the application, for example `https://cauldron.io/`
    - **Redirect URI**: This is important. It should be the Homepage URL and `/meetup-login`. For example, for your local computer: `https://localhost:9000/meetup-login`. (You can change it later)
    - Fill the other fields according with your situation and read and accept the terms and conditions.

</details>

### Configure the variables for your hosts:

**NOTE**: This repository allows you to deploy Cauldron on a single machine or on two machines, the latter being the Elasticsearch service with a dedicated host. Depending on the deployment you choose, you will need to make some extra adjustments to the configuration.

Create a copy of the directory `playbooks/inventories/template`. This directory contains all the variables that could be different for each host. From the root of this repository:
``` bash
$ cd playbooks/inventories
$ cp -r template local
```
Open the file `playbooks/inventories/local/group_vars/all.yml` and fill the configuration. From the root of this repository:
``` bash
$ <prefered_editor> playbooks/inventories/local/group_vars/all.yml
```

- **Oauth application keys** (configure at least one backend):

    <details>
    <summary>More</summary>

    - `gh_client_id` and `gh_client_secret`: GitHub `Client ID` and `Client Secret`
    - `gl_client_id` and `gl_client_secret`: GitLab `Application ID` and `Secret`
    - `meetup_client_id` and `meetup_client_secret`: Meetup `Application ID` and `Secret`

    </details>

- **Base configuration:**
    <details>
    <summary>More</summary>

    - `CAULDRON_CONFIG_DIR`(`/tmp/cauldron-data`): location where the configuration files for the containers will be stored.
    - `HATSTALL_ENABLED`(`false`): by default personal user information collected from the data sources is anonymized. If you want to see and manage user data from [Hatstall](https://github.com/chaoss/grimoirelab-hatstall) set this to True.
    - `NUM_WORKERS`(5): number of [workers](https://gitlab.com/cauldronio/cauldron-worker/) that analyze repositories concurrently.
    - `ELASTIC_HOST` (`elastic_service`): IP address where the Elasticsearch service is hosted or, for single machine deployments, the name of the Elasticsearch Docker container.
    - `CAULDRON_PORT` (9000): port where Cauldron webserver will be running. Use 443 in production.
    - `MATOMO_PORT` (9001): port where Matomo will be running.
    - `ENABLE_PORT_80` (false): if true, petitions to port 80 will be redirected to `https://location:CAULDRON_PORT`
    - `DJANGO_HOSTS` ('*'): location where cauldron is running to avoid HTTP Host header attacks.
    - `ELASTIC_MEMORY` ('4gb'): [head size](https://www.elastic.co/guide/en/elasticsearch/reference/current/heap-size.html) used by Elasticsearch. It is recommended to be half of your RAM.
    - `GOOGLE_ANALYTICS_ID` (''): set the correspoding ID to have analytics.

    </details>

- **Passwords:**
    <details>
    <summary>More</summary>

    - `DB_USER_PASSWORD`('test-password'): password for database
    - `DB_MATOMO_PASSWORD`('test-password'): password for Matomo's table in the database
    - `MATOMO_PASSWORD`('test-password'): password for accessing Matomo
    - `ELASTIC_ADMIN_PASSWORD`('test-password'): password for Elasticsearch admin
    - `ELASTIC_LOGSTASH_PASSWORD`('test-password'): password for Elasticsearch Logstash
    - `ELASTIC_KIBANASERVER_PASSWORD`('test-password'): password for Elasticsearch Kibanaserver
    - `ELASTIC_KIBANARO_PASSWORD`('test-password'): password for Elasticsearch Kibanaro
    - `ELASTIC_READALL_PASSWORD`('test-password'): password for Elasticsearch readall
    - `ELASTIC_SNAPSHOTRESTORE_PASSWORD`('test-password'): password for Elasticsearch snapshotrestore

    </details>

- **Docker volumes** (could be either a path or a Docker volume):
    <details>
    <summary>More</summary>

    - `DB_MOUNT_POINT`('database_volume'): database storage
    - `PROJECT_LOGS_MOUNT_POINT`('cauldron_logs_volume'): logs of repository analysis
    - `ELASTIC_MOUNT_POINT`('elastic_data_volume'): elastic data
    - `ELASTIC_SNAPSHOT_MOUNT_POINT`('elastic_snapshots'): elastic snapshots
    - `PERCEVAL_REPOS_MOUNT_POINT`('perceval_repos'): location for git clone of repositories
    - `SYSLOG_MOUNT_POINT`('syslog_volume'): location for logs storage
    - `MATOMO_MOUNT_POINT`('matomo_volume'): location for storing Matomo configuration

    </details>

- **Administrators for Cauldron**.
    <details>
    <summary>More</summary>

    If you create an account in Cauldron with the username of a data source defined here, you will automatically be an administrator of Cauldron:
    - `GITHUB_ADMINS`([])
    - `GITLAB_ADMINS`([])
    - `MEETUP_ADMINS`([])

    </details>

- **Other variables**

    <details>
    <summary>Docker images</summary>

    - `DB_IMAGE_NAME`("cauldronio/database:latest")
    - `WEB_IMAGE_NAME`("cauldronio/webserver:latest")
    - `WORKER_IMAGE_NAME`("cauldronio/worker:latest")
    - `ODFE_CONFIG_IMAGE_NAME`("cauldronio/odfe-config:latest")
    - `ELASTIC_IMAGE_NAME`("amazon/opendistro-for-elasticsearch:1.4.0")
    - `KIBANA_IMAGE_NAME`("amazon/opendistro-for-elasticsearch-kibana:1.4.0")
    - `SYSLOG_IMAGE_NAME`("cauldronio/syslog-ng:latest")

    </details>

    <details>
    <summary>Docker container names</summary>

    **IMPORTANT**: never change these variables unless you know what you are doing.

    - `DB_CONTAINER_NAME`('db_cauldron_service')
    - `WEB_CONTAINER_NAME`('cauldron_service')
    - `WORKER_CONTAINER_NAME`('worker_service')
    - `ELASTIC_CONTAINER_NAME`('elastic_service')
    - `KIBANA_CONTAINER_NAME`('kibana_service')
    - `NGINX_CONTAINER_NAME`('nginx_service')
    - `SYSLOG_CONTAINER_NAME`('syslog_service')
    - `ODFE_CONFIG_CONTAINER_NAME`('odfe_config_cauldron')
    - `MATOMO_CONTAINER_NAME` ('matomo_service')

    </details>

    <details>
    <summary>Development</summary>

    - `WEB_MOUNT_CODE`: define this variable when you want to test changes on the webserver container without the need to create a new image.
    - `WORKER_MOUNT_CODE`: define this variable when you want to test changes on the worker container without the need to create a new image.
    - `WEB_IMAGE_LOCAL_CODE`: define this variable when you want to build the webserver image with your local code.
    - `WORKER_IMAGE_LOCAL_CODE`: define this variable when you want to build the worker image with your local code.

    </details>

### Target machine for deployment

With the default configuration, Cauldron will run at localhost. If you want to define a diferent location for deploying Cauldron, modify the file `playbooks/inventories/local/hosts`. From the root of this repository:
``` bash
$ <prefered_editor> playbooks/inventories/local/hosts
```
Some variables defined:
- `ansible_connection`(local): ssh for remote host
- `ansible_host`(localhost): define the IP or domain
- `ansible_ssh_user`: user used to deploy cauldron in a remote machine
- `ansible_python_interpreter`

A complete list of the variables that can be defined can be found [here](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#connecting-to-hosts-behavioral-inventory-parameters)

### Create the certificates for your deployment machine.

All the certificates used are located inside `playbooks/files/cauldron_host`.

You have to generate at least self-signed certificates. To do that, browse to the mentioned directory and run `generate.sh`. From the root of this repository:

```bash
$ cd playbooks/files/cauldron_host
$ ./generate.sh  
```
One of the most important certificates generated is `ssl_server`, it is used for the authentication of your public machine. If you use a self-signed certificate, the default case, users will be advised about the insecurity of your site. Please, try to obtain a trusted-signed certificate in order to make your site a safest place.

**IMPORTANT**: If you are going to deploy Cauldron on two different hosts, you must duplicate the `playbooks/files/cauldron_host` directory, and name the copy as `playbooks/files/elasticsearch_host`. From the root of this repository:

```bash
$ cd playbooks/files
$ cp -r cauldron_host elasticsearch_host
```

Also, you will need to modify the file `hosts` from your inventory in order to rename the new host as `elasticsearch_host`.

For more information about Opendistro certificates, you can access the following link for more details: [OpenDistro Certificates](https://opendistro.github.io/for-elasticsearch-docs/docs/security-configuration/generate-certificates/)

### Define your own set of dashboards for your project.

If you want to define some default visualizations for your deployment, you can include them in `files/cauldron_host/kibana_objects`. Only exported `*.ndjson` files from Kibana 7.X are supported. More information at [Kibana saved objects](https://www.elastic.co/guide/en/kibana/current/managing-saved-objects.html).


## Run and stop Cauldron

Once you have defined the variables for Cauldron, navigate to `playbooks` directory from the root of the repository.

```bash
$ cd playbooks
```
There you will find some useful Ansible playbooks for running Cauldron.

### Run Cauldron
``` bash
$ ansible-playbook -i inventories/local cauldron.yml
```
It will deploy Cauldron in the specified hosts in the inventory file. All the images will be pulled from [DockerHub](https://hub.docker.com/u/cauldronio):
- Create Docker network
- Run Cauldron web interface in Docker
- Run ElasticSearch (OpenDistro) in Docker
- Run Kibana (OpenDistro) in Docker
- Run MariaDB in Docker
- Run syslog for centralized logs
- Run Matomo for log analytics
- Create default configuration for Elasticsearch and Kibana, and import visualizations
- (optional) Run Hatstall for managing identities
- Run nginx as a proxy for the containers

### Stop Cauldron
This command will stop and remove all the containers created, but the state will be kept
``` bash
$ ansible-playbook -i inventories/local rm_containers.yml
```

### Cleanup Cauldron
This command will remove all the content created in Cauldron:
``` bash
$ ansible-playbook -i inventories/local rm_volumes.yml
```
The configuration files are stored in the directory defined by `CAULDRON_CONFIG_DIR`. You can safely delete that directory when Cauldron is not running.

## Matomo analytics

Cauldron is using syslog-ng + Matomo for managing the logs. Some steps are necessary to have Matomo correctly configured.

### Installation steps

Go to the port you have Matomo deployed (9001 by default) and follow the installation steps:
1. Welcome (next)
2. System check (next)
3. Database setup. The variables should be defined (next)
4. Creating tables (next)
5. Super User. Specify the user (`MATOMO_USER`) and password (`MATOMO_PASSWORD`) defined in Cauldron's configuration file and your email address. (next)
6. Setup the website to track:
    - Name: Cauldron
    - Website url: your website location
    - Time zone: location where you are
    - Not an Ecommerce site
7. JS Tracking code (next)
8. Congratulations (next)  

Now you can get logs in Matomo. We have configured Matomo with a buffer of 50 hits. You won't see anything until 50 requests are made to the server.


## Advanced deployment for Cauldron

<details>

<summary>More</summary>

Now we will detail all the steps for running Cauldron and the variables that can be modified.

All the playbooks are tagged, therefore you can run them with the flag `-t` and any of the following keyworks: `webserver`, `worker`, `elastic`, `kibana`, `database`, `nginx`, `odfe-config`

- **Build the images.**

  All the images are available in DockerHub with the latest stable version, but you can build them locally with `build_images.yml`. It builds all the images necessary for Cauldron. The Dockerfiles are inside the `docker` directory in the root of this repository. You can modify or overwrite the variables for a specific host in `inventories/<name>/group_vars`. The most important variables are:
    - `XYZ_IMAGE_NAME`: Name for the image
    - `WEB_LOCAL_CODE`/`WORKER_LOCAL_CODE`: Define this variable for including your local code in  the image that you want to create. By default the code is cloned from the repository and included in the image.

  A complete list of the variables used are described in `build_images.yml`.

  For running this playbook execute the following command:
  > Tags available for this playbook are: `webserver`, `worker`, `database`, `odfe-config`

  ``` bash
  $ ansible-playbook -i inventories/local build_images.yml
  ```

  You can see the images created:
  ```bash
  $ docker images
  REPOSITORY               TAG        IMAGE ID           CREATED           SIZE
  cauldronio/odfe-config    X          aaabbbccc11        1 hour ago        925MB
  cauldronio/worker         X          aaabbbccc22        1 hour ago        1.03GB
  cauldronio/webserver      X          aaabbbccc33        1 hour ago        1.05GB
  cauldronio/database       X          aaabbbccc44        1 hour ago        553MB
  ...                      ...        ...                ...                ...
  ```
  You can push the images created to DockerHub with [docker push](https://docs.docker.com/engine/reference/commandline/push/)


- **Create the Cauldron internal network.**

  You can change the name of the network in `inventories/<xxx>/group_vars/all.yml`: `NETWORK_NAME`

  ``` bash
  $ ansible-playbook -i inventories/local create_network.yml
  ```

  You can see the network created:
  ``` bash
  $ docker network ls
  NETWORK ID         NAME                DRIVER              SCOPE
  aaabbbccc55        network_cauldron    bridge              local
  ...                 ...                 ...                 ...
  ```


- **Create configuration files for containers**

    In this step we will create all the configuration files for Cauldron. This files will be stored in the directory defined by `CAULDRON_CONFIG_DIR`. That variable can be modified for each host. Run the following command:

    > Tags available for this playbook are: `webserver`, `worker`, `elastic`, `kibana`, `database`, `nginx`, `odfe-config`

    ```bash
    $ ansible-playbook -i inventories/local create_setup_files.yml
    ```

    This will create in the host and directory defined in your inventory the following directories and files:
    ```
  cauldron-data
  ├── bcrypt-env
  ├── database
  │   └── database.sql
  ├── django
  │   └── django_settings.py
  ├── es
  │   ├── elasticsearch-secured.yml
  │   ├── internal_users.yml
  │   ├── keys
  │   │   ├── admin-key.pem
  │   │   ├── admin.pem
  │   │   ├── node-1-key.pem
  │   │   ├── node-1.pem
  │   │   ├── root-ca-key.pem
  │   │   ├── root-ca.pem
  │   │   └── root-ca.srl
  │   └── opendistro-config.yml
  ├── jwt_key
  │   ├── jwtR256.key
  │   ├── jwtR256.key.pub
  │   └── pub.jwtR256.key
  ├── kibana_objects
  │   └── all_objects.ndjson
  ├── kibana
  │   └── kibana.yml
  ├── mordred
  │   ├── setup-default.cfg
  │   └── worker_config.py
  ├── nginx
  │   ├── certificates
  │   │   ├── ssl_server.crt
  │   │   └── ssl_server.key
  │   └── nginx_cauldron.conf
  └── odfe-config
      └── settings.py
    ```

- **Run Cauldron**

    In this last step we run the Cauldron containers.

    > Tags available for this playbook are: `webserver`, `worker`, `elastic`, `kibana`, `database`, `nginx`, `odfe-config`

    ``` bash
    $ ansible-playbook -i inventories/local run_containers.yml
    ```

    Once it has finished, you can see the running containers:
    ```bash
    $ docker ps
    CONTAINER ID        IMAGE                              COMMAND                  ...   PORTS                            NAMES
    abcdefghij01        cauldronio/worker:X                 "python3 manager.py"     ...                                    worker_service_4
    abcdefghij02        cauldronio/worker:X                 "python3 manager.py"     ...                                    worker_service_3
    abcdefghij03        cauldronio/worker:X                 "python3 manager.py"     ...                                    worker_service_2
    abcdefghij04        cauldronio/worker:X                 "python3 manager.py"     ...                                    worker_service_1
    abcdefghij05        cauldronio/worker:X                 "python3 manager.py"     ...                                    worker_service_0
    abcdefghij06        cauldronio/webserver:X              "/entrypoint.sh"         ...   8000/tcp                         cauldron_service
    abcdefghij07        nginx:latest                        "nginx -g 'daemon of…"   ...   80/tcp, 0.0.0.0:9000->9000/tcp   nginx_service
    abcdefghij08        amazon/opendi...arch-kibana:1.4.0   "/usr/local/bin/kiba…"   ...                                    kibana_service
    abcdefghij09        amazon/opendi..arch:1.4.0           "/usr/local/bin/dock…"   ...   9200/tcp, 9300/tcp, 9600/tcp     elastic_service
    abcdefghij10        cauldronio/database:X               "/entrypoint.sh"         ...   3306/tcp                         db_cauldron_service
    ```

    If everything works correctly, you can **Analyze** some repositories at https://localhost:9000

  If it doesn't work, check the **Troubleshooting** section, below.

- **Stop and remove**.

  - Stop and remove all the containers running:
    > Tags available for this playbook are: `webserver`, `worker`, `elastic`, `kibana`, `database`, `nginx`, `hatstall`

    ```bash
    $ ansible-playbook -i inventories/local rm_containers.yml
    ```
  - Remove network:

    ```bash
    $ ansible-playbook -i inventories/local rm_network.yml
    ```

  - Remove volumes:
    > Tags available for this playbook are: `project_logs`, `elastic`, `elastic_snapshot`,  `database`, `nginx`, `repositories`, `hatstall`

    ```bash
    $ ansible-playbook -i inventories/local rm_volumes.yml
    ```

</details>


## Development environment

For running your Django and Worker local code in the container for development purposes, you need to define the location of the code with the variables `WEB_MOUNT_CODE` and `WORKER_MOUNT_CODE`. If this variables are not defined the containers will use the code from the images.

## Continuous Delivery and Rolling Upgrades

Ansible Playbooks are designed to be idempotent, in this way, you can run the same playbook as many times as you wish and there will not be changes if you didn't modify anything.

In case you modify any of the variables, the playbook will update the configuration variables and take the necessary actions. For example, if you modify the image tag for the web server, it will pull the new image (if it is not stored locally) and update the container with the new version.


> TODO:
> - Include documentation for certbot (git add playbook)

## Admin page

Cauldron comes with an admin page you can use to monitor the status of the server. To access this feature navigate to `/admin-page`, but you will need a user with superuser privileges.

To make the creation of superusers easier, Cauldron provides variables in the inventory file for defining them. Add to the corresponding list the id of the users you want as administrator. You can manage it later from the admin page. For example:

```
GITHUB_ADMINS: ['alice', 'bob']
```

Cauldron also provideds a Django custom command to promote an existing user to a superuser. For example, if you want to convert the user `alice` into a superuser, you should execute the following command:

```py
python3 manage.py promote alice
```

**NOTE**: The command `promote` will set to True the flags `is_staff` and `is_superuser`, so the user promoted will be able to access the Django admin site too.


## Backups

It is important to configure Cauldron to generate periodic snapshots and database backups. If you are not familiar with snapshots, we recommend to read [this article first](https://www.elastic.co/guide/en/elasticsearch/reference/7.x/snapshot-restore.html).

### Database backup
You can create a backup of the Cauldron database with the following command:
```
docker exec db_cauldron mysqldump --all-databases > cauldron_sqldump_test.sql
```

You can restore the database with the following command:
```
cat cauldron_sqldump_test.sql | docker exec -i db_cauldron_service /usr/bin/mysql
```

### Elasticsearch snapshots

In Cauldron, Elasticsearch is configured by default with a snapshot repository that is mounted in the location defined in the inventory's variable `ELASTIC_SNAPSHOT_MOUNT_POINT`.

For creating a snapshot, run inside Elasticsearch container:
```
curl -k -u admin:PASSWORD -XPUT "https://localhost:9200/_snapshot/cauldron_backup/snapshot_test" -H 'Content-Type: application/json' -d'
{
    "indices": "*",
    "ignore_unavailable": true,
    "include_global_state": false
}
'
```
This will created a snapshot with all the indices named `snapshot_test`.

You can see the snapshots created in a remote machine with the script `list_snapshots.py` located in `playbooks/scripts`:
```
python3 list_snapshots.py --ssh user@host --password ELASTIC_ADMIN_PASSWORD
```

You can recover from a snapshot deleting/closing the indices you want to restore and executing the following command inside the Elasticsearch container:
```
curl -k --cert config/admin.pem --key config/admin-key.pem -u admin:PASSWORD -XPOST "https://localhost:9200/_snapshot/cauldron_backup/cauldron_snapshot/_restore" -H 'Content-Type: application/json' -d'
{
  "indices": "INDICES_TO_RESTORE",
  "ignore_unavailable": true,
  "include_global_state": false
}
'
```
You can also move all the indices to a new cluster. Remember to use the same password and jwt certificates in order to work. You need to follow the next steps:
- Run Cauldron in the new machine with:
    ```
    ansible-playbook -i inventories/newlocation cauldron.yml --skip-tags worker,nginx
    ```
- Remove all the indices created. From inside Elasticsearch container run:
    ```
    curl -k --cert config/admin.pem --key config/admin-key.pem -u admin:PASSWORD -XDELETE "https://localhost:9200/*"
    ```
- Restore all the data from a specific snapshot. From inside Elasticsearch container run:
    ```
    curl -k --cert config/admin.pem --key config/admin-key.pem -u admin:PASSWORD -XPOST "https://localhost:9200/_snapshot/cauldron_backup/SNAPSHOT_NAME/_restore" -H 'Content-Type: application/json' -d'
	 {
	    "ignore_unavailable": true,
	    "include_global_state": false
	 }
	 '
    ```
- Wait all the indices green:
    ```
    curl -k -u admin:PASSWORD -XGET "https://localhost:9200/_cat/indices" 2>/dev/null | grep yellow
    ```
- Restart Cauldron from zero:
    ```
    ansible-playbook -i inventories/newlocation rm_containers.yml cauldron.yml
    ```

With both database backup and Elastic snapshot, you can recover the state of Cauldron.

## Help!

In case you have any problem with the deployment or you think this guide is incomplete, open a new issue or contact us please.


## Troubleshooting

### My playbook exits after running ElasticSearch

If it's the first time running Cauldron in your computer and ElasticSearch
exits before finishing the playbook
(check with `docker ps -a --filter "name=elastic_service"`),
it is likely that the `vm.max_map_count` kernel setting needs
to be set to at least **262144**.

This is a likely cause of the playbook ending after 10 attempts to
"run securityadmin to initialize Open Distro Security", which will produce
the following output in your screen:

```
TASK [run_cauldron : Run securityadmin to initialize Open Distro Security] *******************************************
FAILED - RETRYING: Run securityadmin to initialize Open Distro Security (10 retries left).
FAILED - RETRYING: Run securityadmin to initialize Open Distro Security (9 retries left).
...
FAILED - RETRYING: Run securityadmin to initialize Open Distro Security (2 retries left).
FAILED - RETRYING: Run securityadmin to initialize Open Distro Security (1 retries left).
fatal: [localhost]: FAILED! => {"attempts": 10, "changed": true, "cmd":
["docker", "exec", "elastic_service", "plugins/opendistro_security/tools/securityadmin.sh", "-cd", "plugins/opendistro_security/securityconfig/", "-cacert", "config/root-ca.pem", "-cert", "config/admin.pem", "-key", "config/admin-key.pem", "-icl", "-nhnv"],
"delta": "0:00:00.028153", "end": "2019-08-02 17:38:51.778859", "msg": "non-zero return code", "rc": 1,
"start": "2019-08-02 17:38:51.750706",
"stderr": "Error response from daemon: Container xxxx is not running",
"stderr_lines": ["Error response from daemon: Container xxxx is not running"],
"stdout": "", "stdout_lines": []}
```

You can check the details with `docker logs elastic_service`,
which will show something like:

```
[2019-08-02T16:18:13,273][INFO ][o.e.b.BootstrapChecks    ] [48xfr6h] bound or publishing to a non-loopback address, enforcing bootstrap checks
ERROR: [1] bootstrap checks failed
[1]: max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
[2019-08-02T16:18:13,313][INFO ][o.e.n.Node               ] [48xfr6h] stopping ...
[2019-08-02T16:18:13,314][INFO ][c.a.o.s.a.s.SinkProvider ] [48xfr6h] Closing InternalESSink
[2019-08-02T16:18:13,317][INFO ][c.a.o.s.a.s.SinkProvider ] [48xfr6h] Closing DebugSink
[2019-08-02T16:18:13,346][INFO ][o.e.n.Node               ] [48xfr6h] stopped
[2019-08-02T16:18:13,346][INFO ][o.e.n.Node               ] [48xfr6h] closing ...
[2019-08-02T16:18:13,370][INFO ][o.e.n.Node               ] [48xfr6h] closed
```

The fix is to increase `vm.max_map_count` in the controlled host.
You can do that on the fly (in Linux-based systems) by:

```bash
sudo sysctl -w vm.max_map_count=262144
```

But the value will be lost when the maching reboots. For a permanent
fix in Debian, produce a file `/etc/sysctl.d/local.conf` with the
following content (or add to it, if it already exists):

```
###################################################################
# Settings for Elasticsearch to run in production mode
vm.max_map_count=262144
```

Then, to put it into effect now:

```bash
sudo sysctl -p /etc/sysctl.d/local.conf
```

[More info in the Elasticsearch guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#docker-cli-run-prod-mode).
