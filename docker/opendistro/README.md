# Open Distro image for Cauldron

This image is based on OpenDistro official image with following changes:
- Include `repository-s3` plugin
- Fix log4j bug

Some changes are based on https://github.com/Bitergia/bitergia-analytics-odfe-elasticsearch

## How to build this image

```bash
$ docker build -t cauldronio/opendistro-for-elasticsearch:1.13.3 .
```
