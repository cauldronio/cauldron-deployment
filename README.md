# Cauldron deployment

This repository contains relevant information for running Cauldron in your own computer or in a specific machine.


### Requirements

It's necessary that you have **Ansible** installed in your computer in order to run the playbook. You can follow [this link](https://docs.ansible.com/ansible/latest/installation_guide/).

The following ports will be used in the target machine. You can change this later in the configuration file.
   
  - **8000.** Cauldron Django server
  - **9200.** ElasticSearch
  - **3306.** MariaDB Database
  - **443.** Kibiter
  

### Download and configure

1. Download this repository with `git clone` and navigate to that directory:
    ```bash
    $ git clone https://gitlab.com/cauldron2/deployment.git
    $ cd deployment 
    ```

2. You will need to fill some **configuration** before running any task.

    - Create a GitHub Oauth App and get the keys. For creating a new Application [follow this link](https://developer.github.com/apps/building-oauth-apps/creating-an-oauth-app/). Some information for the application:
        - **Application name**: A name for the application, for example `Bitergia Cauldron`
        - **Homepage URL**: This should be the full URL to your application homepage. If you will run it in your local computer, you can type `http://localhost:8000/`. (You can change it later)
        - **Application description**: Not required
        - **Authorization callback URL**: This is important. It should be the Homepage URL and `/github-login`. For example, for your local computer: `http://localhost:8000/github-login`. (You can change it later)
        
        After the registration, you can obtain the `Client ID` and `Client Secret`.
    
    - Open the following file (inside the cloned repository) with a text editor: 
        ```
        playbooks/roles/cauldron/defaults/main.yml
        ```
        - You will need to write you GitHub Oauth keys (`gh_client_id` and `gh_client_secret`).
        
        You can leave the other configuration as it is, but there are some points that could be interesting:
        - Some configuration files for Docker containers will be mounted in the local filesystem. Now are in `/tmp` because of permissions. If you want another directory, you can modify it with the `configuration_dir` option. 
        - If you are using any of the mentioned ports before (443, 8000, 9200 or 3306), you can change them here. By default is **3**, but you can change it before running at any time.
        - You can select how many workers for mordred will be running in the `num_workers` option. 

### Running
Navigate to `playbooks` directory from the root of the repository.

```
$ cd playbooks
```
There are some useful **playbooks**:

- **`install_docker.yml`**. **Only** run this playbook if you don't have Docker installed in the target machine for running the Cauldron. It will install Docker and its dependencies.
    ```
    $ ansible-playbook install_docker.yml 
    ```
    If you are running it for localhost, you need to be root (append `-K` to the previous command and it will ask for your password)

- **`build_images.yml`**. If you don't have the images for the Cauldron web server and the Mordred worker in the target computer, you will need to build them:
    ```bash
    $ ansible-playbook build_images.yml
    ```
    It builds the Dockerfile inside `cauldron` and `mordred` that are in this repository.
    
    You can see the images created:
    ```bash
    $ docker images
    REPOSITORY              TAG                 IMAGE ID            CREATED             SIZE
    mordred                 latest              9b33c908fcb6        10 seconds ago      895MB
    cauldron                latest              36302776d1b7        30 seconds ago      1.09GB
    ...
    ```

- **`run_cauldron.yml`**. With this playbook you will be able to:
    - Run the Docker images: `cauldron`, `mordred` and `grimoirelab/secured`
    - Create a Docker network (`network_cauldron` by default)
    - Create a Docker volume (`cauldron_volume` by dafault)
    ```bash
    $ ansible-playbook run_cauldron.yml
    ```
    Once it has finished, you can see the running containers and the volume and network created:
    ```
    $ docker ps
    CONTAINER ID        IMAGE                 COMMAND                  CREATED             STATUS              PORTS                                                                   NAMES
    78c3c33a89f0        mordred               "python3 manager.py"     14 seconds ago      Up 13 seconds                                                                               mordred_service_2
    58078aaee172        mordred               "python3 manager.py"     16 seconds ago      Up 14 seconds                                                                               mordred_service_1
    85d7b93c72f0        mordred               "python3 manager.py"     18 seconds ago      Up 16 seconds                                                                               mordred_service_0
    e4ee49ee77a5        cauldron              "/entrypoint.sh"         21 seconds ago      Up 19 seconds       0.0.0.0:8000->8000/tcp                                                  cauldron_service
    eccb4c735aaf        grimoirelab/secured   "/entrypoint.sh -c /…"   23 seconds ago      Up 21 seconds       0.0.0.0:3306->3306/tcp, 0.0.0.0:9200->9200/tcp, 0.0.0.0:443->5601/tcp   grimoirelab_service         
    
    $ docker volume ls
    NETWORK ID          NAME                DRIVER              SCOPE
    b9a99d39aa1c        network_cauldron    bridge              local
    ...

    $ docker network ls
    DRIVER              VOLUME NAME
    local               cauldron_volume

    ```
    If everythink works correctly, you can:
    
    - **Analyze** some repositories at http://localhost:8000
    - Use **Kibiter** for your dashboard at https://localhost
    - Browse the data analyzed in a **ElasticSearch**: https://localhost:92000 

- **`stop_cauldron.yml`**. With this playbook you can remove all the containers and images generated.

    ```bash
    $ ansible-playbook stop_cauldron.yml
    ```

### Help!

In case you have any problem with the deployment or you think this guide is incomplete, open a new issue or contact us please.
