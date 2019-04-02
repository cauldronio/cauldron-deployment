# Cauldron deployment

This repository contains relevant information for running Cauldron in your own computer or in a specific machine.


### Requirements

It's necessary that you have **Ansible** installed in your computer in order to run the playbook. You can follow [this link](https://docs.ansible.com/ansible/latest/installation_guide/).


### Installation

1. Clone this repository in your workout directory.
    ```
    $ git clone https://gitlab.com/cauldron2/deployment.git
    ```
    
    Fill the file inside the repository: `cauldron/settings_secret.py`. You will need:
      
    - Create a [Github Oauth App](https://developer.github.com/apps/building-oauth-apps/creating-an-oauth-app/) and get the keys. Note: For the _Authorization callback URL_ write `http://localhost:8000/github-login` if you are going to run the container in your local machine.

    - Generate a new Django secret key with `openssl rand -base64 32`.

2. Run Cauldron using Ansible tasks

    > **IMPORTANT**. If you have docker installed, omit the 'install Docker' step with ` --skip-tags "install_docker"`.  In some cases it will install Docker and you will have 2 instances of Docker running.
    
    There are 2 files for deploying and running Cauldron depending on the target:
    - Run Cauldron in your **local** machine:
        
        ```
        $ ansible-playbook deploy-cauldron.yml -K
        ```
         The `-K` is for allowing Ansible to install docker in your machine (it will ask for your password).
         
        If all tasks completed successfully, you can visit the homepage at http://localhost:8000
    
    - Run Cauldron in a **remote** machine
    
        You should have access with `ssh` and your public key shoud be in `authorized_keys`.
        ```
        $ ansible-playbook -i IP, deploy-cauldron-remote.yml
        ```
               
        You will have to change Django's `ALLOWED_HOSTS` to allow your IP.
        
    
    
In case you have any problem with the deployment or you think this guide is incomplete, open a new issue or contact us please.
