import logging
import requests
import json
import time
import ssl
import os

from elasticsearch import Elasticsearch
from elasticsearch.connection import create_ssl_context

import settings

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


LOG_FORMAT = "[%(asctime)s - %(levelname)s] %(message)s"
ELASTIC_URL = f"{settings.ES_IN_PROTOCOL}://{settings.ES_IN_HOST}:{settings.ES_IN_PORT}"
KIBANA_URL = f"{settings.KIB_IN_PROTOCOL}://{settings.KIB_IN_HOST}:{settings.KIB_IN_PORT}{settings.KIB_PATH}"

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
Logger = logging.getLogger("configuration")


def wait_for_elastic():
    headers = {'Content-Type': 'application/json'}

    while True:
        Logger.info("Waiting for Elastic...")
        try:
            r = requests.get(ELASTIC_URL,
                             auth=('admin', settings.ES_ADMIN_PASSWORD),
                             verify=False,
                             headers=headers)
        except requests.exceptions.ConnectionError:
            Logger.warning("Connection error. Retry in 5 seconds")
            time.sleep(5)
            continue
        if r.ok:
            Logger.info("Connected to Elastic")
            break
        time.sleep(5)


def wait_for_kibana():
    headers = {'Content-Type': 'application/json'}

    while True:
        Logger.info("Waiting for Kibana...")
        try:
            r = requests.get(f'{KIBANA_URL}/api/status',
                             headers=headers)
        except requests.exceptions.ConnectionError:
            Logger.warning("Connection error. Retry in 5 seconds")
            time.sleep(5)
            continue
        if r.ok and r.text == "Kibana server is not ready yet":
            Logger.warning(f"{r.text}. Retry in 5 seconds")
            time.sleep(5)
            continue
        if r.ok:
            Logger.info("Connected to Kibana")
            break
        time.sleep(5)


def connect_elasticsearch():
    context = create_ssl_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    es = Elasticsearch([settings.ES_IN_HOST], scheme=settings.ES_IN_PROTOCOL, port=settings.ES_IN_PORT,
                       http_auth=("admin", settings.ES_ADMIN_PASSWORD), ssl_context=context)
    while not es.ping():
        Logger.warning("Connection to Elastic failed... Retry")
    return es


def import_kibana_object(path):
    """
    This method import the object defined in path in Kibana using saved_objects API
    :param path: *.ndjson file path to be imported in Kibana
    :return:
    """
    Logger.info(f'Importing {path}')

    headers = {'kbn-xsrf': 'true',
               'securitytenant': 'global'}
    saved_objects_api = f"{settings.KIB_IN_PROTOCOL}://{settings.KIB_IN_HOST}:{settings.KIB_IN_PORT}{settings.KIB_PATH}" \
                        f"/api/saved_objects/_import?overwrite=true"
    files = {'file': open(path, 'rb')}

    r = requests.post(saved_objects_api,
                      auth=('admin', settings.ES_ADMIN_PASSWORD),
                      verify=False,
                      files=files,
                      headers=headers)
    Logger.info(f'{r.status_code} - {r.json()}')


def import_kibana_objects(location):
    """
    This method import all the objects inside location
    """
    Logger.info('Import Kibana objects')

    for root, _, files in os.walk(location):
        for name in files:
            if name.endswith('.ndjson'):
                import_kibana_object(os.path.join(root, name))

    Logger.info("Kibana objects successfully created")


def default_index_pattern(index_pattern):
    Logger.info("Creating index pattern")

    headers = {'Content-Type': 'application/json', 'kbn-xsrf': 'true'}
    r = requests.post(f'{KIBANA_URL}/api/kibana/settings/defaultIndex',
                      auth=("admin", settings.ES_ADMIN_PASSWORD),
                      json={"value": index_pattern},
                      verify=False,
                      headers=headers)
    if r.ok:
        Logger.info("Index pattern created")
    else:
        Logger.info(f"Index pattern creation failed: {r.status_code}: {r.text}")


def create_indices(es):
    Logger.info('Creating default indices')

    with open('mappings/git_aoc.json') as json_file:
        git_aoc_mapping = json.load(json_file)

    with open('mappings/gitlab.json') as json_file:
        gitlab_mapping = json.load(json_file)

    es.indices.create('git_raw_index', ignore=400)
    es.indices.create('git_enrich_index', ignore=400)
    es.indices.create('git_aoc_enriched_index', body=git_aoc_mapping, ignore=400)
    es.indices.create('github_raw_index', ignore=400)
    es.indices.create('github_enrich_index', ignore=400)
    # es.indices.create('github_pull_enrich_index', ignore=400)
    # es.indices.create('github_pull_raw_index', ignore=400)
    es.indices.create('github_repo_enrich_index', ignore=400)
    es.indices.create('github_repo_raw_index', ignore=400)
    es.indices.create('github2_enrich_index', ignore=400)
    # es.indices.create('github2_pull_enriched_index', ignore=400)
    es.indices.create('gitlab_raw_index', ignore=400)
    es.indices.create('gitlab_enriched_index', body=gitlab_mapping, ignore=400)
    es.indices.create('gitlab_mrs_raw_index', ignore=400)
    es.indices.create('gitlab_mrs_enriched_index', ignore=400)
    es.indices.create('meetup_raw_index', ignore=400)
    es.indices.create('meetup_enriched_index', ignore=400)

    Logger.info('Default indices created')


def create_aliases(es):
    Logger.info('Creating aliases...')
    es.indices.put_alias(index='git_aoc_enriched_*', name='git_aoc_enriched')
    es.indices.put_alias(index='git_enrich_*', name='git_enrich')
    es.indices.put_alias(index='github_enrich_*', name='github_enrich')
    # es.indices.put_alias(index='github_pull_enrich_*', name='github_pull_enrich')
    es.indices.put_alias(index='github_repo_enrich_*', name='github_repo_enrich')
    es.indices.put_alias(index='gitlab_enriched_*', name='gitlab_enriched')
    es.indices.put_alias(index='gitlab_mrs_enriched_*', name='gitlab_mrs_enriched')
    es.indices.put_alias(index='meetup_enriched_*', name='meetup_enriched')
    es.indices.put_alias(index='git_enrich_*', name='ocean')
    es.indices.put_alias(index='github_enrich_*', name='ocean')
    es.indices.put_alias(index='gitlab_enriched_*', name='ocean')
    es.indices.put_alias(index='gitlab_mrs_enriched_*', name='ocean')
    es.indices.put_alias(index='meetup_enriched_*', name='ocean')
    es.indices.put_alias(index='github_enrich_*', name='ocean_tickets')
    es.indices.put_alias(index='gitlab_enriched_*', name='ocean_tickets')
    es.indices.put_alias(index='gitlab_mrs_enriched_*', name='ocean_tickets')
    es.indices.put_alias(index='meetup_enriched_*', name='ocean_tickets')
    Logger.info('Aliases created')


def set_snapshot_location(location):
    Logger.info('Defining snapshot location for ElasticSearch')

    headers = {'Content-Type': 'application/json',
               'kbn-xsrf': 'true'}
    data_snapshot = {
        "type": "fs",
        "settings": {
            "location": location
        }
    }

    req = requests.put(f'{ELASTIC_URL}/_snapshot/cauldron_backup',
                       auth=('admin', settings.ES_ADMIN_PASSWORD),
                       verify=False,
                       headers=headers,
                       json=data_snapshot)

    Logger.info(f'{req.status_code} - {req.json()}')


def update_max_scrolls(num_scrolls):
    Logger.info('Updating number of max open scrolls')

    headers_scrolls = {'Content-Type': 'application/json'}
    data_scrolls = {
        "persistent": {
            "search.max_open_scroll_context": num_scrolls
        },
        "transient": {
            "search.max_open_scroll_context": num_scrolls
        }
    }
    req = requests.put(f'{ELASTIC_URL}/_cluster/settings',
                       auth=('admin', settings.ES_ADMIN_PASSWORD),
                       verify=False,
                       headers=headers_scrolls,
                       json=data_scrolls)
    Logger.info(f'{req.status_code} - {req.json()}')


def update_max_shards(num_shards):
    Logger.info('Updating number of max shards per node')

    headers_shards = {'Content-Type': 'application/json'}
    data_shards = {
        "persistent": {
            "cluster.max_shards_per_node": "3000"
        }
    }
    req = requests.put(f'{ELASTIC_URL}/_cluster/settings',
                       auth=('admin', settings.ES_ADMIN_PASSWORD),
                       verify=False,
                       headers=headers_shards,
                       json=data_shards)
    Logger.info(f'{req.status_code} - {req.json()}')


if __name__ == "__main__":
    wait_for_elastic()
    wait_for_kibana()
    elastic = connect_elasticsearch()
    update_max_shards(2000)
    import_kibana_objects('./kibana_objects')
    default_index_pattern('git_enrich')
    create_indices(elastic)
    create_aliases(elastic)
    set_snapshot_location("/mnt/snapshots")
    update_max_scrolls(5000)

