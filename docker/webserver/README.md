# Cauldron webserver

**IMPORTANT NOTE**
> You can build and run this image, but you will end up doing a lot of work manually.
> We recommend you to use the Ansible playbooks specially created for deploying Cauldron local or remotely



### Build image

#### Prepare the context
The Dockerfile creates a image with Cauldron webserver installed

You have to clone/copy the desired code you want to run inside `src`. For example, for running the latest version you can:

```bash
$ cd docker/webserver
$ git clone https://gitlab.com/cauldronio/cauldron-web src
```

Or you can copy the code from another location into `src`. Remember that the contents of the repository should be inside `src`:

```bash
$ ls src
Cauldron2  LICENSE  README.md  requirements.txt  ...
```

#### Build!

```bash
$ docker build -t cauldron_server_image .
```



### Run

The web server needs some services running:
- Database running
- ElasticSearch running
- A common volume or directory with the workers for the logs

It also needs:
- A custom `settings.py`
- JSON Web Token private key.

There is a example settings file inside the `example-files` directory and a script for creating the JSON Web Token.

For running the container you will need the following command:
```
docker run  --name cauldron_container \
                     --network cauldron_network \ # Optional
                     -v "example/settings.py:/code/cauldron/Cauldron2/Cauldron2/settings.py" \
                     -v "logs_volume:/dashboard_logs" \
                     -v "example/jwtR256.key:/code/cauldron/Cauldron2/CauldronApp/jwtR256.key"
```
