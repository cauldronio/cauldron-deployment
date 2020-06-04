# Performance Analyzer to Elasticsearch Docker image

This image is for build a Docker container that collects some of the metrics
surfaced by Performance Analyzer, across some dimensions and aggregations. It
pushes those metrics to Elasticsearch for visualization with Kibana.

## How to run this image

- Requirements:
  - Elasticsearch cluster configured and running
  - [Index template](https://gitlab.com/cauldronio/pa-to-es/-/blob/master/template7.json) imported to your cluster

- Build the image:
```bash
$ docker build -t pa-to-es:test .
```

- Run the image
```bash
$ docker run --name pa-to-es -e "ELASTIC_HOST=elastic_service" -e "ELASTIC_PASSWORD=test-password" --network network_cauldron pa-to-es:test
```
