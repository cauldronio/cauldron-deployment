# Cauldron deployment

This repository contains relevant information for running Cauldron in your own computer or in a specific machine.


### Requirements

It's necessary that you have **Ansible** installed in your computer in order to run the playbook. You can follow [this link](https://docs.ansible.com/ansible/latest/installation_guide/).

The following ports will be used in the target machine:
   
  - **8000.** Cauldron Django server
  - **9200.** ElasticSearch
  - **3306.** MariaDB Database
  - **443.** Kibiter
  

### Installation

1. Download this repository with `git clone` in your desired directory and get into it:
    ```bash
    $ git clone https://gitlab.com/cauldron2/deployment.git
    $ cd deployment 
    ```

2. You will need to fill some **configuration** before running any task.

    - Create a [Github Oauth App](https://developer.github.com/apps/building-oauth-apps/creating-an-oauth-app/) and get the keys.
        - **Application name**: A name for you and your users, like `Bitergia Cauldron`
        - **Homepage URL**: This should be the full URL to your application homepage. If you will run it in your own machine you can write `http://localhost:8000/`. (You can change it later)
        - **Application description**: Not required
        - **Authorization callback URL**: This is important. It should be the Homepage URL and `/github-login`. For example, for your local machine: `http://localhost:8000/github-login`. (You can change it later)
        
        After the registration you need to get the  `Client ID` and `Client Secret`.
    
    - Open the following file (inside the cloned repository) with a text editor: 
        ```
        cauldron-playbooks/roles/cauldron/defaults/main.yml
        ```
        - You will need to write you `GitHub Oauth` keys (`gh_client_id` and `gh_client_secret`).
        
        You can leave the other configuration as it is, but there are some points that could be interesting:
        - Some configuration files for Docker containers will be mounted in the local filesystem. Now are in `/tmp` because of permissions. If you want another directory, you can modify it with the `configuration_dir` option. 
        - If you are using any of the mentioned ports before (443, 8000, 9200 or 3306), you can change them here. Be careful with the 443 port, because it will ask for a secure connection.
        - You can select how many workers for mordred will be running in the `num_workers` option. 

3. Navigate to `cauldron-playbooks` directory from the root of the repository. There are some useful playbooks:

    - **`install_docker.yml`*+. **Only** run this playbook if you don't have Docker installed in the computer that you want to run the Cauldron. It will install all the dependencies for Docker and run it.
        ```
        $ ansible-playbook install_docker.yml 
        ```
        If you are running it for localhost, you need to be root (append `-K` to the previous command and it will ask for your password)
        
    - **`build_images.yml`**. If you don't have the images for the Cauldron web server and the Mordred worker in your computer, you will need to build them:
        ```bash
        $ ansible-playbook build_images.yml
        ```
        It builds the images that are in this repository, in `cauldron` and `mordred` directories.
        
        You can see the images created with:
        ```bash
        $ docker images
        REPOSITORY              TAG                 IMAGE ID            CREATED             SIZE
        mordred                 latest              9b33c908fcb6        10 seconds ago      895MB
        cauldron                latest              36302776d1b7        30 seconds ago      1.09GB
        ...
        ```
        
    - **`run_cauldron.yml`**. With this playbook you will run the previous generated images, `grimoirelab/secured`, create a Docker network and a Docker volume for sharing information.
        ```bash
        $ ansible-playbook run_cauldron.yml
        ```
        Once it has finished, you can see the running containers:
        ```
        $ docker ps
        CONTAINER ID        IMAGE                 COMMAND                  CREATED             STATUS              PORTS                                                                   NAMES
        78c3c33a89f0        mordred               "python3 manager.py"     14 seconds ago      Up 13 seconds                                                                               mordred_service_2
        58078aaee172        mordred               "python3 manager.py"     16 seconds ago      Up 14 seconds                                                                               mordred_service_1
        85d7b93c72f0        mordred               "python3 manager.py"     18 seconds ago      Up 16 seconds                                                                               mordred_service_0
        e4ee49ee77a5        cauldron              "/entrypoint.sh"         21 seconds ago      Up 19 seconds       0.0.0.0:8000->8000/tcp                                                  cauldron_service
        eccb4c735aaf        grimoirelab/secured   "/entrypoint.sh -c /…"   23 seconds ago      Up 21 seconds       0.0.0.0:3306->3306/tcp, 0.0.0.0:9200->9200/tcp, 0.0.0.0:443->5601/tcp   grimoirelab_service         
        ```
        If everythink works correctly, you can access http://localhost:8000 and analyze some of repositories. You can see the results in ElasticSearch at https://localhost:92000 with the default user and password (admin:admin) or you can go to Kibiter https://localhost
        
     - **`stop_cauldron.yml`**. With this playbook you can remove all the containers and images generated.
        ```bash
        $ ansible-playbook stop_cauldron.yml
        ```


In case you have any problem with the deployment or you think this guide is incomplete, open a new issue or contact us please.
