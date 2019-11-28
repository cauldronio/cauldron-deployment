# Cauldron deployment

This repository contains relevant information for running Cauldron in your own computer or in a specific machine.


## Requirements

- It's necessary that you have **Ansible** (~2.8) installed in your computer in order to run the playbooks. You can follow [this link](https://docs.ansible.com/ansible/latest/installation_guide/) to find the installation docs.

  **NOTE**: Ansible works by default with your system's default Python version, but it is possible to change it. Anyway, please check your Ansible configuration to be sure about which Python version is being used by executing:
  ```bash
   $ ansible --version
  ```

- **Docker** (~18.09) is also needed for running the containers. You can install it by following [this link](https://docs.docker.com/install/).

  **IMPORTANT**: You will also need to add your own user to the docker group created during the installation of Docker in order to execute Docker CLI without `sudo`:
  ```bash
   $ sudo usermod -aG docker $USER
  ```

- **Docker SDK for Python** is required by Ansible to execute Docker commands in Python scripts. Depending on your Ansible's Python version you will need to execute the following:

  - **Python <= 2.6**
  ```bash
     $ pip install docker-py
  ```

  - **Python 2.7 and > 3**
  ```bash
     $ pip install docker
     # or
     $ pip3 install docker
  ```

- **virtualenv** is necessary for creating a Python environment for generating the hashed keys for OpenDistro for ElasticSearch:
  ``` bash
    virtualenv --version
  ```

- **rsync** is necessary for copying the files to a remote machine. To check if you have it installed:
  ``` bash
    rsync --version
  ```

- The following ports will be used in the target machine. You can change this later in the configuration file.

  - **9000**: Cauldron web interface


## Clone and configure

1. Download the latest version of this repository with `git clone` and navigate to that directory:
     ```bash
    $ git clone https://gitlab.com/cauldron2/cauldron-deployment.git
    $ cd cauldron-deployment
    ```

2. Create Oauth application keys for each backend or the those that you want to use:

    - Create a **GitHub Oauth App** and get the keys. For creating a new Application [follow this link](https://developer.github.com/apps/building-oauth-apps/creating-an-oauth-app/). Some information for the application:
        - **Application name**: A name for the application, for example `Bitergia Cauldron`
        - **Homepage URL**: This should be the full URL to your application homepage. If you will run it in your local computer, you can type `https://localhost:9000/`. (You can change it later)
        - **Application description**: Not required
        - **Authorization callback URL**: This is important. It should be the Homepage URL and `/github-login`. For example, for your local computer: `https://localhost:9000/github-login`. (You can change it later)

        After the registration, you can obtain the `Client ID` and `Client Secret`.

    - Create a **Gitlab Oauth App** and get the keys. For creating a new Application [follow this link](https://docs.gitlab.com/ee/integration/oauth_provider.html#adding-an-application-through-the-profile). Some information for the application:
        - **Name**: A name for the application, for example `Bitergia Cauldron`
        - **Redirect URI**: This is important. It should be the Homepage URL and `/gitlab-login`. For example, for your local computer: `https://localhost:9000/gitlab-login`. (You can change it later)
        - **Scopes**: Select only `api`

        After the registration, you can obtain the `Application ID` and `Secret`.

    - ~~Create a **Meetup Oauth App** and get the keys. For creating a new Application [follow this link](https://secure.meetup.com/meetup_api/oauth_consumers/create/).~~ **Meetup API has changed and you cannot create free applications anymore. We keep this section if you have already one for testing the site**. Some information for the application:
        - **Consumer Name**: A name for the application, for example `Bitergia Cauldron`
        - **Application website**: A website for the application, for example `https://cauldron2.gitlab.io/`
        - Request access for personal use if you are going to deploy locally, request for organization if you are going to deploy it publicly (The second may take some days to be accepted).
        - **Redirect URI **: This is important. It should be the Homepage URL and `/meetup-login`. For example, for your local computer: `https://localhost:9000/meetup-login`. (You can change it later)
        - **Phone number and Description**: this is for accepting the application, provide some description.
        Finally read and accept the terms and conditions. After the registration, you can obtain the `Application ID` and `Secret`

3. Change **Cauldron variables** for your host:

    - If you want to run Cauldron locally, rename (or duplicate) the directory `template` inside playbooks/inventories as `local`. This directory contains all the variables that could be different for each host.
        ``` bash
        $ cd playbooks/inventories
        $ cp -r template local
        ```

    - *Only if you want to change the host*: open the file `playbooks/inventories/local/hosts` and modify the variables included. [You can also add another variables defined in this link](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#connecting-to-hosts-behavioral-inventory-parameters).

    - Finally change the variables related to Cauldron. Open the file `playbooks/inventories/local/host_vars/cauldron_host.yml` and fill the configuration:
        ``` bash
        $ <prefered_editor> local/host_vars/cauldron_host.yml
        ```
        - Fill the Oauth keys:
          - Your GitHub Oauth keys (`gh_client_id` and `gh_client_secret`).
          - Your Gitlab Oauth keys (`gl_client_id` and `gl_client_secret`).
          - *Only if you have the Meetup keys*: Your Meetup Oauth keys (`meetup_client_id` and `meetup_client_secret`).

        - Define if you want Hatstall enabled and the use of Sortinghat with `HATSTALL_ENABLED`

        - You can leave the other configuration as it is, but there are some variables that could be interesting:

          - Some configuration files for containers will be stored in the target host. The default directory is `/tmp/cauldron-data` because of permissions. If you want another directory, you can modify it with the `CAULDRON_CONFIG_DIR` option.
          - You can select how many workers for mordred will be running in the `NUM_WORKERS` option. By default is **5**, but you can change it.
          - If you are using the port 9000, you can change it here. For production, use the port 443 and set `ENABLE_PORT_80` to true (only for nginx redirects).
          - If you are going to run Cauldron in a public IP is important that you change some of the passwords. The default is: `test-password`.

4. Create/change the certificates for your deployment machine.

    All the certificates used are located inside `playbooks/files/cauldron_host`.

    You have to generate at least self-signed certificates. To do that, browse to the mentioned directory and run `generate.sh`:

    ```bash
    $ cd playbooks/files/cauldron_host
    $ ./generate.sh  
    ```
    One of the most important certificates generated is `ssl_server`, it is used for the authentication of your public machine. If you use a self-signed certificate, the default case, users will be advised about the insecurity of your site. Please, try to obtain a trusted-signed certificate in order to make your site a safest place.

    For more information about each certificate, you can access the following link for more details: [OpenDistro Certificates](https://opendistro.github.io/for-elasticsearch-docs/docs/security-configuration/generate-certificates/)

## Run for impatients

Navigate to `playbooks` directory from the root of the repository.

```bash
$ cd playbooks
```
There you will find some useful Ansible playbooks for running Cauldron. If you just want to **run Cauldron**, run the following command:
  ``` bash
  $ ansible-playbook -i inventories/local cauldron.yml
  ```
  It will deploy Cauldron in the specified host in the inventory file. All the images will be pulled from [DockerHub](https://hub.docker.com/u/cauldron2):
  - Create Docker network
  - Run Cauldron web interface in Docker
  - Run ElasticSearch (OpenDistro) in Docker
  - Run Kibana (OpenDistro) in Docker
  - Run MariaDB in Docker
  - Import default panels for Kibana

## Run Step by step

Now we will detail all the steps for running Cauldron and the variables that can be modified.

All the playbooks are tagged, therefore you can run them with the flag `-t` and any of the following keyworks: `webserver`, `worker`, `elastic`, `kibana`, `database`, `nginx`, `panels`

- **Build the images.**

  All the images are available in DockerHub with the latest stable version, but you can build them locally with `build_images.yml`. It builds all the images necessary for Cauldron. The Dockerfiles and inside the `docker` directory in the root of this repository. You can modify or overwrite the variables for a specific host in `inventories/<name>/host_vars`. The most important variables are:
    - `XYZ_IMAGE_NAME`: Name for the image
    - `WEB_LOCAL_CODE`/`WORKER_LOCAL_CODE`: Define this variable for including your local code in  the image that you want to create. By default the code is cloned from the repository and included in the image.

  A complete list of the variables used are described in `build_images.yml`.

  For running this playbook execute the following command:
  > Tags available for this playbook are: `webserver`, `worker`, `database`, `panels`

  ``` bash
  $ ansible-playbook -i inventories/local build_images.yml
  ```

  You can see the images created:
  ```bash
  $ docker images
  REPOSITORY               TAG        IMAGE ID           CREATED           SIZE
  cauldron2/panels         X          aaabbbccc11        1 hour ago        925MB
  cauldron2/worker         X          aaabbbccc22        1 hour ago        1.03GB
  cauldron2/webserver      X          aaabbbccc33        1 hour ago        1.05GB
  cauldron2/database       X          aaabbbccc44        1 hour ago        553MB
  ...                      ...        ...                ...                ...
  ```
  You can push the images created to DockerHub with [docker push](https://docs.docker.com/engine/reference/commandline/push/)


- **Create the Cauldron internal network.**

  You can change the name of the network in `inventories/<xxx>/host_vars/<yyy>`: `NETWORK_NAME`

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

    > Tags available for this playbook are: `webserver`, `worker`, `elastic`, `kibana`, `database`, `nginx`, `panels`

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
  └── panels
      └── settings.py
    ```

- **Run Cauldron**

    In this last step we run the Cauldron containers.

    > Tags available for this playbook are: `webserver`, `worker`, `elastic`, `kibana`, `database`, `nginx`, `panels`

    ``` bash
    $ ansible-playbook -i inventories/local run_containers.yml
    ```

    Once it has finished, you can see the running containers:
    ```bash
    $ docker ps
    CONTAINER ID        IMAGE                              COMMAND                  ...   PORTS                            NAMES
    abcdefghij01        cauldron2/worker:X                 "python3 manager.py"     ...                                    worker_service_4
    abcdefghij02        cauldron2/worker:X                 "python3 manager.py"     ...                                    worker_service_3
    abcdefghij03        cauldron2/worker:X                 "python3 manager.py"     ...                                    worker_service_2
    abcdefghij04        cauldron2/worker:X                 "python3 manager.py"     ...                                    worker_service_1
    abcdefghij05        cauldron2/worker:X                 "python3 manager.py"     ...                                    worker_service_0
    abcdefghij06        cauldron2/webserver:X              "/entrypoint.sh"         ...   8000/tcp                         cauldron_service
    abcdefghij07        nginx:latest                       "nginx -g 'daemon of…"   ...   80/tcp, 0.0.0.0:9000->9000/tcp   nginx_service
    abcdefghij08        amazon/opendi...arch-kibana:0.9.0  "/usr/local/bin/kiba…"   ...                                    kibana_service
    abcdefghij09        amazon/opendi..arch:0.9.0          "/usr/local/bin/dock…"   ...   9200/tcp, 9300/tcp, 9600/tcp     elastic_service
    abcdefghij10        cauldron2/database:X               "/entrypoint.sh"         ...   3306/tcp                         db_cauldron_service
    ```

    If everything works correctly, you can **Analyze** some repositories at https://localhost:9000

  If it doesn't work, check the **Troubleshooting** section, below.

- **Stop and remove**.

  - Stop and remove all the containers running:
  > Tags available for this playbook are: `webserver`, `worker`, `elastic`, `kibana`, `database`, `nginx`

    ```bash
    $ ansible-playbook -i inventories/local rm_containers.yml
    ```
  - Remove network:

    ```bash
    $ ansible-playbook -i inventories/local rm_network.yml
    ```

  - Remove volumes:
  > Tags available for this playbook are: `logs`, `elastic`, `database`

    ```bash
    $ ansible-playbook -i inventories/local rm_volumes.yml
    ```

## Development environment

For running your Django and Worker local code in the container for development purposes, you need to define the location of the code with the variables `WEB_MOUNT_CODE` and `WORKER_MOUNT_CODE`. If this variables are not defined the containers will use the code from the images.


> TODO:
> - Script for remove configuration
> - Include documentation for certbot (git add playbook)

## Admin page

Cauldron comes with an admin page you can use to monitor the status of the server. To access this feature navigate to `/admin-page`, but you will need a user with superuser privileges.

To make the creation of superusers easier, Cauldron provides a Django custom command to promote an existing user to a superuser. For example, if you want to convert the user `alice` into a superuser, you should execute the following command:

```py
python3 manage.py promote alice
```

**NOTE**: The command `promote` will set to True the flags `is_staff` and `is_superuser`, so the user promoted will be able to access the Django admin site too.

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

## Contributing

### Ansible Documentation

Feel free to participate in the creation of the Cauldron's Ansible documentation by sharing any modification that you consider relevant to the project! Please, follow these guidelines in order to homogenize the docs:

- We are using the tool [ansible-autodoc](https://pypi.org/project/ansible-autodoc/) to generate documents in a semi-automatic way. Please, refer to its documentation to learn how to use it.

  **NOTE**: Currently, [ansible-autodoc](https://pypi.org/project/ansible-autodoc/) is not totally adapted to our document specifications. It is planned for the future to make a fork and modify it ([Issue related](https://gitlab.com/cauldron2/cauldron-deployment/issues/8)). For now, every `README.md` generated by the tool will be modified by us to adapt it. You cant take a look to this Issue.
