# Cauldron post-configuration for Elasticsearch and Kibana (Opendistro)

This image is used for configuring Elasticsearch and Kibana for Cauldron. This is part of the deployment and is not supposed to be run outside that context.

This image perform the following tasks:
- Wait for Elasticsearch running
- Wait for Kibana running
- Import index templates
- Import kibana objects (visualizations, dashboards, index patterns...)
- Define a default index pattern
- Create default indices and mappings for Sirmordred
- Create aliases for the indices
- Set the snapshot location for the Elastic container
- Update the max number of scrolls

Mapping files for the indices are in the `mappings` directory.

The settings for connecting to ElasticSearch and Kibana are defined in `settings.py` file. _It is overwritten in the deployment_.

All the kibana objects are stored in the `kibana_objects` directory. _It is overwritten in the deployment_.

## How to run outside deployment
This container is not supposed to be run outside the deployment context. If you want to do it:
- Build the image:
```bash
$ docker build -t odfe-config:test .  
```
- Fill the `settings.py` file with the variables defined
- Add some kibana objects (`*.ndjson` files compatible with `7.X`) in `kibana_objects` directory

- Run the image
```bash
$ docker run --name test-odfe-config -v settings.py:/settings.py -v kibana_objects:/kibana_objects
```
