# Cauldron worker

**IMPORTANT NOTE**
> You can build and run this image, but you will end up doing a lot of work manually.
> We recommend you to use the Ansible playbooks specially created for deploying workers local or remotely



### Build image

#### Prepare the context
The Dockerfile creates a image with a worker installed that consume tasks

You have to clone/copy the desired code you want to run inside `src`. For example, for running the latest version you can:

```bash
$ cd docker/worker
$ git clone https://gitlab.com/cauldronio/cauldron-worker src
```

Or you can copy the code from another location into `src`. Remember that the contents of the repository should be inside `src`:

```bash
$ ls src
LICENSE  MordredManager  README.md  requirements.txt  ...
```

#### Build!

```bash
$ docker build -t cauldron_worker_image .
```



### Run

The worker needs some services running:
- Database running
- ElasticSearch running
- A common volume or directory with the webserver for the logs

It also needs:
- `setup.cfg` for Mordred tasks
- `config.py` with the passwords for accessing the database

There are example files inside the `example-files` directory.

For running the container you will need the following command:
```
docker run  --name cauldron_worker_0 \
                     --network cauldron_network \ # Optional
                     -v "example-files/config.py:/code/MordredManager/config.py" \
                     -v "logs_volume:/dashboard_logs" \
                     -v "example-files/setup.cfg:/code/MordredManager/mordred/setup-default.cfg"
```
