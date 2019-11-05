from archimedes.archimedes import Archimedes
import logging
import requests
import settings
import ssl
import json
from elasticsearch import Elasticsearch
from elasticsearch.connection import create_ssl_context
import time

# Create the logger
log_format = logging.Formatter("[%(name)s] %(asctime)s [%(levelname)s] %(message)s", "%d-%m-%Y %H:%M:%S")
log_handler = logging.StreamHandler()
log_handler.setLevel(logging.DEBUG)
log_handler.setFormatter(log_format)
Logger = logging.getLogger("panels")
Logger.addHandler(log_handler)
Logger.setLevel(logging.DEBUG)


# --- Wait for ES Running --- #
while True:
    Logger.info("Waiting for ES...")
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.get("{}".format(settings.ES_IN_URL),
                         auth=('admin', settings.ES_ADMIN_PSW),
                         verify=False,
                         headers=headers)
    except requests.exceptions.ConnectionError:
        Logger.warning("Connection error. Retry in 5 seconds")
        time.sleep(5)
        continue
    if r.ok:
        Logger.info("Connected to ES")
        break
    time.sleep(5)


# --- Create instance of ES --- #
context = create_ssl_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
es = Elasticsearch([settings.ES_IN_HOST], scheme=settings.ES_PROTO, port=settings.ES_PORT,
                   http_auth=("admin", settings.ES_ADMIN_PSW), ssl_context=context)

while not es.ping():
    Logger.warning("Connection failed... Retry")


# --- Import index patterns --- #
Logger.info('Import Index patterns')
kib_url_auth = "{}://admin:{}@{}:{}{}".format(settings.KIB_IN_PROTO,
                                              settings.ES_ADMIN_PSW,
                                              settings.KIB_IN_HOST,
                                              settings.KIB_IN_PORT,
                                              settings.KIB_PATH)

archimedes = Archimedes(kib_url_auth, '/panels')
archimedes.import_from_disk(obj_type='dashboard', obj_id='8c34bc50-a2fe-11e9-ac51-1516462fb85e',
                            find=True, force=False)
archimedes.import_from_disk(obj_type='dashboard', obj_id='4434c9a0-18dd-11e9-ba47-d5cbef43f8d3',
                            find=True, force=False)
archimedes.import_from_disk(obj_type='dashboard', obj_id='69208f40-18cb-11e9-ba47-d5cbef43f8d3',
                            find=True, force=False)
archimedes.import_from_disk(obj_type='dashboard', obj_id='b7b169e0-14e3-11e9-8aac-ef7fd4d8cbad',
                            find=True, force=False)
archimedes.import_from_disk(obj_type='dashboard', obj_id='b7df3b10-a195-11e9-8e03-59480d72fd0a',
                            find=True, force=False)
archimedes.import_from_disk(obj_type='dashboard', obj_id='Meetup',
                            find=True, force=False)

Logger.info("Panels successfully created")

# --- Set default index pattern ---#
Logger.info('Set default index pattern')
headers = {'Content-Type': 'application/json', 'kbn-xsrf': 'true'}
r = requests.post('{}/api/kibana/settings/defaultIndex'.format(settings.KIB_IN_URL),
              auth=("admin", settings.ES_ADMIN_PSW),
              json={"value": "git_enrich"},
              verify=False,
              headers=headers)
Logger.info("{} - {}".format(r.status_code, r.text))


# --- Copy panels and index patters to Global index ---#
# Logger.info("Copy panels from {} to Global .kibana".format("admin"))
# es.reindex(body={"source": {"index": ".kibana_*_admin"}, "dest": {"index": ".kibana"}})


# --- Create default indices to avoid warning when a visualization does not exist ---#
Logger.info('Add some default indices')

body = dict()
with open('git_aoc.json') as json_file:
    body = json.load(json_file)

es.indices.create('git_raw_index', ignore=400)
es.indices.create('git_enrich_index', ignore=400)
es.indices.create('git_aoc_enriched_index', body=body, ignore=400)
es.indices.create('github_raw_index', ignore=400)
es.indices.create('github_enrich_index', ignore=400)
es.indices.create('gitlab_raw_index', ignore=400)
es.indices.create('gitlab_enriched_index', ignore=400)
es.indices.create('meetup_raw_index', ignore=400)
es.indices.create('meetup_enriched_index', ignore=400)


def put_alias_no_except(es_obj, index, name):
    try:
        es_obj.indices.put_alias(index=index, name=name)
    except es.NotFoundError:
        pass


put_alias_no_except(es, index='git_aoc_enriched_*', name='git_aoc_enriched')
put_alias_no_except(es, index='git_enrich_*', name='git_enrich')
put_alias_no_except(es, index='github_enrich_*', name='github_enrich')
put_alias_no_except(es, index='gitlab_enriched_*', name='gitlab_enriched')
put_alias_no_except(es, index='meetup_enriched_*', name='meetup_enriched')
put_alias_no_except(es, index='git_enrich_*', name='ocean')
put_alias_no_except(es, index='github_enrich_*', name='ocean')
put_alias_no_except(es, index='gitlab_enriched_*', name='ocean')
put_alias_no_except(es, index='meetup_enriched_*', name='ocean')
put_alias_no_except(es, index='github_enrich_*', name='ocean_tickets')
put_alias_no_except(es, index='gitlab_enriched_*', name='ocean_tickets')
put_alias_no_except(es, index='meetup_enriched_*', name='ocean_tickets')
Logger.info('Default indices added')