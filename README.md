# Cauldron deployment

This repository contains relevant information for running Cauldron in your own computer or in a specific machine.


### Requirements

It's necessary that you have **Ansible** installed in your computer in order to run the playbook. You can follow [this link](https://docs.ansible.com/ansible/latest/installation_guide/).

The following ports will be used in the target machine. You can change this later in the configuration file.
   
  - **8000.** Cauldron Django server
  - **9200.** ElasticSearch
  - **443.** Kibana
  

### Download and configure

1. Download the latest tagged version of this repository with `git clone --branch tag` and navigate to that directory:
    ```bash
    $ git clone --branch <tag> https://gitlab.com/cauldron2/deployment.git
    $ cd deployment 
    ```
    **Or** you can download the latest version in **development**:
     ```bash
    $ git clone https://gitlab.com/cauldron2/deployment.git
    $ cd deployment 
    ```

2. You will need to fill some **configuration** before running any task.

    - Create a **GitHub Oauth App** and get the keys. For creating a new Application [follow this link](https://developer.github.com/apps/building-oauth-apps/creating-an-oauth-app/). Some information for the application:
        - **Application name**: A name for the application, for example `Bitergia Cauldron`
        - **Homepage URL**: This should be the full URL to your application homepage. If you will run it in your local computer, you can type `http://localhost:8000/`. (You can change it later)
        - **Application description**: Not required
        - **Authorization callback URL**: This is important. It should be the Homepage URL and `/github-login`. For example, for your local computer: `http://localhost:8000/github-login`. (You can change it later)
        
        After the registration, you can obtain the `Client ID` and `Client Secret`.
        
    - Create a **Gitlab Oauth App** and get the keys. For creating a new Application [follow this link](https://docs.gitlab.com/ee/integration/oauth_provider.html#adding-an-application-through-the-profile). Some information for the application:
        - **Name**: A name for the application, for example `Bitergia Cauldron`
        - **Redirect URI**: This is important. It should be the Homepage URL and `/gitlab-login`. For example, for your local computer: `http://localhost:8000/gitlab-login`. (You can change it later)
        - **Scopes**: Select only `api`
        
        After the registration, you can obtain the `Application ID` and `Secret`.
     
    - Create a private gitlab token (This is a temporary step until some changes are applied to perceval). [Gitlab personal access tokens](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#creating-a-personal-access-token) 

    - Open the following file (inside the cloned repository) with a text editor: 
        ```
        playbooks/defaults.yml
        ```
        - You will need to write:
          - Your GitHub Oauth keys (`gh_client_id` and `gh_client_secret`).
          - Your Gitlab Oauth keys (`gl_client_id` and `gl_client_secret`).
          - Your Gitlab private token (`gl_private_token`)
        
        You can leave the other configuration as it is, but there are some points that could be interesting:
        - If you are going to run Cauldron in a public IP is important that you change some of the passwords: `db_root_password`, `db_password` and `es_admin_password` are the most important.
        - Some configuration files for Docker containers will be mounted in the local filesystem. Now are in `/tmp` because of permissions. If you want another directory, you can modify it with the `configuration_dir` option. 
        - If you are using any of the mentioned ports before (443, 8000 or 9200), you can change them here. 
        - You can select how many workers for mordred will be running in the `num_workers` option. By default is **3**, but you can change it before running at any time.

### Running
Navigate to `playbooks` directory from the root of the repository.

```
$ cd playbooks
```
There are some useful **playbooks**. You will need a custom inventory. There are 2 example files: one for a remote machine `production` and another one for your local machine: `local`:

- **`install_docker.yml`**. **Only** run this playbook if you don't have Docker installed in the target machine for running the Cauldron. It will install Docker and its dependencies.
    ```
    $ ansible-playbook -i <inventory_file> install_docker.yml 
    ```
    If you are running it for localhost, you need to be root (append `-K` to the previous command and it will ask for your password)

- **`configure_cauldron.yml`**. You will need to run this playbook the first time. This playbook will:
    - Create a internal Docker Network
    - Create a Docker Volume
    - Create the Django configuration and copy to remote
    - Build Django image 
    - Build Mordred image
    - Build Database image
    - Create the Database configuration
    - Create OpenDistro configuration
    - Pull mysql image
    - Copy panels for Kibana

    The command for running this playbook is:
    ```bash
    $ ansible-playbook -i <inventory_file> configure_cauldron.yml
    ```
    It builds the Dockerfile inside `cauldron` and `mordred` that are in this repository.
    
    You can see the images created:
    ```bash
    $ docker images
    REPOSITORY              TAG                 IMAGE ID            CREATED             SIZE
    mordred                 latest              9b33c908fcb6        10 seconds ago      895MB
    cauldron                latest              36302776d1b7        10 seconds ago      1.09GB
    database_cauldron       latest              293e6e74dd4b        10 seconds ago      553MB
    mysql                   latest              990386cbd5c0        10 seconds ago      443MB
    ...
    ```
    An the configuration created by default in `/tmp/database`, `/tmp/django`, `/tmp/kibana`, `/tmp/mordred`, `/tmp/panels` and `tmp/panels`
- **`run_cauldron.yml`**. With this playbook you will be able to run the Docker images: `cauldron`, `mordred` and `grimoirelab/secured`
    ```bash
    $ ansible-playbook -i <inventory_file> run_cauldron.yml
    ```
    Once it has finished, you can see the running containers and the volume and network created:
    ```bash
    $ docker ps
    CONTAINER ID        IMAGE                                              COMMAND                  CREATED             STATUS              PORTS                                                      NAMES
    81fc9f917120        amazon/opendistro-for-elasticsearch:0.9.0          "/usr/local/bin/dock…"   5 hours ago         Up 5 hours          0.0.0.0:9200->9200/tcp, 0.0.0.0:9600->9600/tcp, 9300/tcp   elastic_service
    0faeb212a4b3        amazon/opendistro-for-elasticsearch-kibana:0.9.0   "/usr/local/bin/kiba…"   5 hours ago         Up 5 hours          0.0.0.0:5601->5601/tcp                                     kibana_service
    8ae30f440689        mordred                                            "python3 manager.py"     5 hours ago         Up 5 hours                                                                     mordred_service_3
    bd3996f77f1c        mordred                                            "python3 manager.py"     5 hours ago         Up 5 hours                                                                     mordred_service_2
    cb4e6dcd27d0        mordred                                            "python3 manager.py"     5 hours ago         Up 5 hours                                                                     mordred_service_1
    e997f0a02e67        mordred                                            "python3 manager.py"     5 hours ago         Up 5 hours                                                                     mordred_service_0
    55cca3a6d1be        cauldron                                           "/entrypoint.sh"         5 hours ago         Up 2 hours          0.0.0.0:80->8000/tcp                                       cauldron_service
    71eb8dc42702        database_cauldron                                  "/entrypoint.sh"         5 hours ago         Up 5 hours          0.0.0.0:3306->3306/tcp                                     db_cauldron_service
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
    
    - **Analyze** some repositories at http://localhost:8000
    - Use **Kibana** for your dashboard at https://localhost:5601
    - Browse the data analyzed in a **ElasticSearch**: https://localhost:92000
    
    You can find the default passwords inside `playbooks/defaults.yml`

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