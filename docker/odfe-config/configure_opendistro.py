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

HEADER_JSON = {'Content-Type': 'application/json'}

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
Logger = logging.getLogger("configuration")


def wait_for_elastic():
    while True:
        Logger.info("Waiting for Elastic...")
        try:
            r = requests.get(ELASTIC_URL,
                             auth=('admin', settings.ES_ADMIN_PASSWORD),
                             verify=False,
                             headers=HEADER_JSON)
        except requests.exceptions.ConnectionError:
            Logger.warning("Connection error. Retry in 5 seconds")
            time.sleep(5)
            continue
        if r.ok:
            Logger.info("Connected to Elastic")
            break
        time.sleep(5)


def wait_for_kibana():
    while True:
        Logger.info("Waiting for Kibana...")
        try:
            r = requests.get(f'{KIBANA_URL}/api/status',
                             headers=HEADER_JSON)
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


def import_kibana_object(kibana_url, admin_password, filename, tenant):
    """
    This method imports the object defined in filename in Kibana using saved_objects API
    :param kibana_url: kibana endpoint
    :param admin_password: admin password for Kibana
    :param filename: *.ndjson file path to be imported in Kibana
    :param tenant: tenant who is going to import the objects
    :return:
    """
    Logger.info(f'Importing {filename}')

    headers = {'kbn-xsrf': 'true',
               'securitytenant': tenant}
    saved_objects_api = f"{kibana_url}/api/saved_objects/_import?overwrite=true"
    with open(filename, 'rb') as f:
        files = {'file': f}
        r = requests.post(saved_objects_api,
                          auth=('admin', admin_password),
                          verify=False,
                          files=files,
                          headers=headers)

        Logger.info(f'{r.status_code} - {r.json()}')


def import_kibana_objects(location, tenant):
    """
    This method import all the objects inside location
    to a specific tenant
    """
    Logger.info(f"Import Kibana objects to {tenant} tenant")

    for root, _, files in os.walk(location):
        for name in files:
            if name.endswith('.ndjson'):
                import_kibana_object(KIBANA_URL, settings.ES_ADMIN_PASSWORD, os.path.join(root, name), tenant)

    Logger.info(f"Kibana objects successfully created in {tenant} tenant")


def load_template(template_file):
    with open(template_file) as f_template:
        try:
            template = json.load(f_template)
        except Exception as e:
            logging.error(e)
            raise
    return template


def import_index_template(path):
    """
    This method imports the index template defined in path in Elasticsearch using REST API
    :param path: *.json file path to be imported in Elasticsearch
    :return:
    """
    Logger.info(f'Importing {path}')

    template = load_template(path)
    template_name = os.path.splitext(os.path.basename(path))[0]

    r = requests.post(f'{ELASTIC_URL}/_template/{template_name}',
                      auth=('admin', settings.ES_ADMIN_PASSWORD),
                      verify=False,
                      headers=HEADER_JSON,
                      data=json.dumps(template))
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.warning(f"Error creating {template_name}. {r.status_code}, {r.text}")
        raise

    Logger.info(f'{template_name} created')


def import_index_templates(location):
    """
    This method imports all the index templates inside location
    """
    Logger.info('Import index templates')

    for root, _, files in os.walk(location):
        for name in files:
            if name.endswith('.json'):
                import_index_template(os.path.join(root, name))

    Logger.info("Index templates successfully created")


def default_index_pattern(index_pattern):
    Logger.info(f"Set {index_pattern} as default index pattern")

    headers = {'Content-Type': 'application/json', 'kbn-xsrf': 'true'}
    r = requests.post(f'{KIBANA_URL}/api/kibana/settings/defaultIndex',
                      auth=("admin", settings.ES_ADMIN_PASSWORD),
                      json={"value": index_pattern},
                      verify=False,
                      headers=headers)

    if not r.ok:
        Logger.error(f"Set default index pattern failed: {r.status_code}: {r.text}")


def create_indices(es):
    Logger.info('Creating default indices')

    # with open('mappings/git_aoc.json') as json_file:
    #     git_aoc_mapping = json.load(json_file)

    with open('mappings/gitlab.json') as json_file:
        gitlab_mapping = json.load(json_file)

    es.indices.create('git_raw_index', ignore=400)
    es.indices.create('git_enrich_index', ignore=400)
    # es.indices.create('git_aoc_enriched_index', body=git_aoc_mapping, ignore=400)
    es.indices.create('github_raw_index', ignore=400)
    es.indices.create('github_enrich_index', ignore=400)
    es.indices.create('github_repo_enrich_index', ignore=400)
    es.indices.create('github_repo_raw_index', ignore=400)
    es.indices.create('github2_enrich_index', ignore=400)
    es.indices.create('gitlab_raw_index', ignore=400)
    es.indices.create('gitlab_enriched_index', body=gitlab_mapping, ignore=400)
    es.indices.create('gitlab_mrs_raw_index', ignore=400)
    es.indices.create('gitlab_mrs_enriched_index', ignore=400)
    es.indices.create('meetup_raw_index', ignore=400)
    es.indices.create('meetup_enriched_index', ignore=400)
    es.indices.create('cauldron_daily_metrics', ignore=400)
    es.indices.create('cauldron_monthly_metrics', ignore=400)

    Logger.info('Default indices created')


def load_aliases(aliases_file):
    with open(aliases_file) as f_aliases:
        try:
            aliases = json.load(f_aliases)
        except Exception as e:
            logging.error(e)
            raise
    return aliases


def create_aliases():
    Logger.info('Creating aliases...')

    aliases = load_aliases('aliases.json')

    for alias_dict in aliases:
        alias_action = {
            "actions": [
                {
                    "add": alias_dict
                }
            ]
        }
        r = requests.post(f'{ELASTIC_URL}/_aliases',
                          auth=('admin', settings.ES_ADMIN_PASSWORD),
                          verify=False,
                          headers=HEADER_JSON,
                          data=json.dumps(alias_action))
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.warning(f"Error creating alias {alias_dict}. {r.status_code}, {r.text}")
            raise

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
                       headers=HEADER_JSON,
                       json=data_scrolls)
    Logger.info(f'{req.status_code} - {req.json()}')


def update_max_shards(num_shards):
    Logger.info('Updating number of max shards per node')

    data_shards = {
        "persistent": {
            "cluster.max_shards_per_node": "3000"
        }
    }
    req = requests.put(f'{ELASTIC_URL}/_cluster/settings',
                       auth=('admin', settings.ES_ADMIN_PASSWORD),
                       verify=False,
                       headers=HEADER_JSON,
                       json=data_shards)
    Logger.info(f'{req.status_code} - {req.json()}')


def enable_performance_analyzer():
    Logger.info("Enabling performance analyzer")

    data_enable = {
        'enabled': True
    }
    req = requests.post(f'{ELASTIC_URL}/_opendistro/_performanceanalyzer/config',
                       auth=('admin', settings.ES_ADMIN_PASSWORD),
                       verify=False,
                       headers=HEADER_JSON,
                       json=data_enable)
    Logger.info(f'{req.status_code} - {req.json()}')


if __name__ == "__main__":
    wait_for_elastic()
    wait_for_kibana()
    elastic = connect_elasticsearch()
    update_max_shards(2000)
    import_index_templates('./index_templates')
    import_kibana_objects('./kibana_objects/global_objects', 'global')
    import_kibana_objects('./kibana_objects/admin_objects', 'admin_tenant')
    default_index_pattern('all')
    create_indices(elastic)
    create_aliases()
    set_snapshot_location("/mnt/snapshots")
    update_max_scrolls(5000)
    enable_performance_analyzer()
