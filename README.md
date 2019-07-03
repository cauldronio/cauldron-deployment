# Cauldron deployment

This repository contains relevant information for running Cauldron in your own computer or in a specific machine.


### Requirements

It's necessary that you have **Ansible** installed in your computer in order to run the playbook. You can follow [this link](https://docs.ansible.com/ansible/latest/installation_guide/).

**Docker** is also needed for running the containers. You can install it following [this link](https://docs.docker.com/install/) 

The following ports will be used in the target machine. You can change this later in the configuration file.
   
  - **9000.** Cauldron server
  

### Download and configure

1. Download the latest version of this repository with `git clone` and navigate to that directory:
     ```bash
    $ git clone https://gitlab.com/cauldron2/deployment.git
    $ cd deployment 
    ```

2. You will need to fill some **configuration** before running any task.

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

    - You need to create a new jwtKey for the authenticated petitions for Kibana from Django. For that you need to run the `generate_jwt_keys.sh`:
         ```bash
        $ ./generate_jwt_keys.sh
        ```
        It will create 2 new files: `jwtR256.key` and `jwtR256.key.pub`. The first one you have to copy into `playbooks/roles/configure_cauldron/files/django`:
        ```bash
        $ cp jwtR256.key playbooks/roles/configure_cauldron/files/django/
        ```
        The second one you have to keep it for the next step.
        
    - Rename the file `template` inside playbooks/group_vars  as `local` and open it with a text editor: 
        ``` bash
        $ cd playbooks
        $ cp group_vars/template group_vars/local
        $ <prefered_editor> group_vars/local
        ```
        - You will need to fill:
          - Your GitHub Oauth keys (`gh_client_id` and `gh_client_secret`).
          - Your Gitlab Oauth keys (`gl_client_id` and `gl_client_secret`).
          - The key previously created inside `jwtR256.key.pub` you have to copy it in the variable `es_jwt_signing_key`.
        
        You can leave the other configuration as it is, but there are some points that could be interesting:
        - If you are going to run Cauldron in a public IP is important that you change some of the passwords: `db_root_password`, `db_password` and `es_admin_password` are the most important.
        - Some configuration files for Docker containers will be mounted in the local filesystem. The default directory is `/tmp` because of permissions. If you want another directory, you can modify it with the `configuration_dir` option. 
        - If you are using any of the mentioned ports before (9000), you can change them here. For production port 443 is desirable and set `enable_port_80` to true (for redirects).  
        - You can select how many workers for mordred will be running in the `num_workers` option. By default is **3**, but you can change it.
      
    - Another important configuration is to change the certificates for your deployment machine. All the certificates used are located inside `playbooks/roles/configure_cauldron/files/keys`. 
      
      By default, there aren't certificates, you have to generate at least self-signed certificates. To do that, browse to the mentioned directory and run `generate.sh`:
    
        ```bash
        $ cd playbooks/roles/configure_cauldron/files/keys
        $ ./generate.sh  
        ```
        One of the most important is certificates is `ssl_server`, it is used for the communication outside the containers. Use a signed certificate for a public machine. (We are working with `certbot`, a playbook will be soon available)
        
        For more information about each certificate, you can access the following link for more details: [OpenDistro Certificates](https://opendistro.github.io/for-elasticsearch-docs/docs/security-configuration/generate-certificates/)
     
3. Finally, it's necessary to have a inventory file for the target machine. If you are running it locally, you can use the `local` file inside `playbooks` directory. 

    IMPORTANT: If you are going to create a new inventory, the name for the group (the header `[]`) must be the same as the name of the file inside `group_vars` that you previously renamed/copied.

### Running
Navigate to `playbooks` directory from the root of the repository.

```bash
$ cd playbooks
```
There you will find some useful files for running Cauldron:

- **`configure_cauldron.yml`**. You will need to run this playbook the first time. This playbook will:
    - Create a Docker Network
    - Create a Docker Volume
    - Create the Django configuration and copy to remote (localhost in this guide)
    - Create the Database configuration
    - Create OpenDistro configuration
    - Copy panels for Kibana
    - Build Django image
    - Build Mordred image
    - Build Database image
    - Build Panels image
    - Pull a mysql image
    - Pull a nginx image
    - Pull Opendistro images, ES and Kibana
    
    You can skip the creation of the images if you have them locally and just want to update the configuration files. Use for that `--skip-tags create_image`. 
 
    The command for running this playbook is:
    ```bash
    $ ansible-playbook -i <inventory_file> configure_cauldron.yml
    ```
    It builds the Dockerfile inside `cauldron` and `mordred` that are in this repository.
    
    You can see the images created:
    ```bash
    $ docker images
    REPOSITORY              TAG                 IMAGE ID            CREATED             SIZE
    mordred                 latest              aaabbbcccdd1        0 seconds ago      922MB
    cauldron                latest              aaabbbcccdd2        0 seconds ago      1.08GB
    database_cauldron       latest              aaabbbcccdd3        0 seconds ago      553MB
    mysql                   latest              aaabbbcccdd4        0 seconds ago      443MB
    nginx                   latest              aaabbbcccdd5        0 seconds ago      109MB
    panels_image            latest              aaabbbcccdd6        0 seconds ago      936MB
    amazon/opendistro-f...  0.9.0               aaabbbcccdd7        0 seconds ago      774MB
    amazon/opendistro-f...  0.9.0               aaabbbcccdd8        0 seconds ago      527MB
    grimoirelab/installed   0.2.23              aaabbbcccdd9        0 seconds ago      889MB
    ...
    ```
    And the configuration created by default in `/tmp/database`, `/tmp/django`, `/tmp/kibana`, `/tmp/mordred`, `/tmp/archimedes_panels`, `/tmp/es` and `/tmp/nginx`.
- **`run_cauldron.yml`**. With this playbook you will be able to run the Docker images: `cauldron`, `mordred`, `database_cauldron`, `nginx` and `opendistro` images
    ```bash
    $ ansible-playbook -i <inventory_file> run_cauldron.yml
    ```
    Once it has finished, you can see the running containers and the volume and network created:
    ```bash
    $ docker ps
    CONTAINER ID        IMAGE                                              COMMAND                  CREATED             STATUS              PORTS                                                      NAMES
    7f72551f5018        nginx                                              "nginx -g 'daemon of…"   5 hours ago         Up 5 hours          80/tcp, 0.0.0.0:9000->9000/tcp                             nginx_service
    81fc9f917120        amazon/opendistro-for-elasticsearch:0.9.0          "/usr/local/bin/dock…"   5 hours ago         Up 5 hours          9200/tcp, 9600/tcp, 9300/tcp                               elastic_service
    0faeb212a4b3        amazon/opendistro-for-elasticsearch-kibana:0.9.0   "/usr/local/bin/kiba…"   5 hours ago         Up 5 hours          5601/tcp                                                   kibana_service
    8ae30f440689        mordred                                            "python3 manager.py"     5 hours ago         Up 5 hours                                                                     mordred_service_3
    bd3996f77f1c        mordred                                            "python3 manager.py"     5 hours ago         Up 5 hours                                                                     mordred_service_2
    cb4e6dcd27d0        mordred                                            "python3 manager.py"     5 hours ago         Up 5 hours                                                                     mordred_service_1
    e997f0a02e67        mordred                                            "python3 manager.py"     5 hours ago         Up 5 hours                                                                     mordred_service_0
    55cca3a6d1be        cauldron                                           "/entrypoint.sh"         5 hours ago         Up 2 hours          8000/tcp                                                   cauldron_service
    71eb8dc42702        database_cauldron                                  "/entrypoint.sh"         5 hours ago         Up 5 hours          3306/tcp                                                   db_cauldron_service
    ...
  
    $ docker volume ls
    NETWORK ID          NAME                DRIVER              SCOPE
    b9a99d39aa1c        network_cauldron    bridge              local
    ...

    $ docker network ls
    DRIVER              VOLUME NAME
    local               cauldron_volume
    ...
    ```
    If everything works correctly, you can:
    
    - **Analyze** some repositories at https://localhost:9000

- **`remove_cauldron.yml`**. With this playbook you can remove all the containers, images, volumes, networks and configuration generated.

    ```bash
    $ ansible-playbook -i <inventory_file> remove_cauldron.yml
    ```

### Help!

In case you have any problem with the deployment or you think this guide is incomplete, open a new issue or contact us please.


## Troubleshooting

#### My playbook exits after running ElasticSearch

If it's the first time running the Cauldron in your computer and ElasticSearch exits before finishing the playbook (`docker ps -a --filter "name=elastic_service"`), it's possible that the `vm.max_map_count` kernel setting needs to be set to at least **262144**:

```bash
sudo sysctl -w vm.max_map_count=262144
```
[More Info](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#docker-cli-run-prod-mode)