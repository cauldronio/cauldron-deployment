# Open Distro image for Cauldron

This image is based on OpenDistro official image with following changes:
- Include `repository-s3` plugin

## How to build this image

```bash
$ ODFE_VERSION=x.x.x
$ docker build --build-arg ODFE_VERSION=$ODFE_VERSION -t cauldronio/opendistro-for-elasticsearch:$ODFE_VERSION .
```
