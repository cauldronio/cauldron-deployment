# Cauldron deployment

This repository contains relevant information for running Cauldron in your own computer or in a specific machine.


### Requirements

It's necessary that you have **Ansible** installed in your computer in order to run the playbook. You can follow [this link](https://docs.ansible.com/ansible/latest/installation_guide/).


### Installation

- Clone this repository in your workout directory.
```
$ git clone https://gitlab.com/cauldron2/deployment.git
```
- Rename the `cauldron/settings_secret_template.py` file to `cauldron/settings_secret.py`. Then, fill that file. You will need:
  - Create a [Github Oauth App](https://developer.github.com/apps/building-oauth-apps/creating-an-oauth-app/) and get the keys.
  - Generate a new Django secret key with `openssl rand -base64 32`.
- For running Cauldron type:
```
$ ansible-playbook deploy-cauldron.yml -K
```
 The `-K` is for allowing Ansible to install some packages in your machine (allow sudo commands).

 In case you have docker installed, you can omit that step with ` --skip-tags "install_docker"`.

- If all the tasks finished correct, you can access http://localhost:8000


In case you have any problem with the deployment or you think this guide is incomplete, open a new issue or contact us please.
