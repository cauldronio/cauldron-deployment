from archimedes.archimedes import Archimedes
import logging
import os
import requests
import settings
import ssl
from elasticsearch import Elasticsearch
from elasticsearch.client import CatClient
from elasticsearch.connection import create_ssl_context


# --- Create ES User --- #
logging.warning('Creating ES user: <{}>'.format(settings.PANELS_USERNAME))
headers = {'Content-Type': 'application/json'}
r = requests.put("{}/_opendistro/_security/api/internalusers/{}".format(settings.ES_IN_URL, settings.PANELS_USERNAME),
                 auth=('admin', settings.ES_ADMIN_PSW),
                 json={"password": settings.PANELS_USER_PSW},
                 verify=False,
                 headers=headers)
logging.warning("{} - {}".format(r.status_code, r.text))

# --- Import index patterns --- #
logging.warning('Import Index patterns')
kib_url_auth = "{}://{}:{}@{}:{}{}".format(settings.KIB_IN_PROTO,
                                           settings.PANELS_USERNAME,
                                           settings.PANELS_USER_PSW,
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

logging.warning("Panels successfully created")

# --- Set default index pattern ---#
logging.warning('Set default index pattern')
headers = {'Content-Type': 'application/json', 'kbn-xsrf': 'true'}
r = requests.post('{}/api/kibana/settings/defaultIndex'.format(settings.KIB_IN_URL),
              auth=(settings.PANELS_USERNAME, settings.PANELS_USER_PSW),
              json={"value": "git_enrich"},
              verify=False,
              headers=headers)
logging.warning("{} - {}".format(r.status_code, r.text))


# --- Create default indices to avoid warning when a visualization does not exist ---#
logging.warning('Add some default indices')
context = create_ssl_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
es = Elasticsearch([settings.ES_IN_HOST], scheme=settings.ES_PROTO, port=settings.ES_PORT,
                   http_auth=("admin", settings.ES_ADMIN_PSW), ssl_context=context)

body = {
    "mappings": {
        "_doc": {
            "properties": {
                "grimoire_creation_date": {
                    "type": "date"
                }
            }
        }
    }
}

es.indices.create('git_raw_index', ignore=400)
es.indices.create('git_enrich_index', ignore=400)
es.indices.create('git_aoc_enriched_index', ignore=400)
es.indices.create('github_raw_index', ignore=400)
es.indices.create('github_enrich_index', ignore=400)
es.indices.create('gitlab_raw_index', ignore=400)
es.indices.create('gitlab_enriched_index', ignore=400)

def put_alias_no_except(es_obj, index, name):
    try:
        es_obj.indices.put_alias(index=index, name=name)
    except es.NotFoundError:
        pass

put_alias_no_except(es, index='git_aoc_enriched_*', name='git_aoc_enriched')
put_alias_no_except(es, index='git_enrich_*', name='git_enrich')
put_alias_no_except(es, index='github_enrich_*', name='github_enrich')
put_alias_no_except(es, index='gitlab_enriched_*', name='gitlab_enriched')
put_alias_no_except(es, index='git_enrich_*', name='ocean')
put_alias_no_except(es, index='github_enrich_*', name='ocean')
put_alias_no_except(es, index='gitlab_enriched_*', name='ocean')
put_alias_no_except(es, index='github_enrich_*', name='ocean_tickets')
put_alias_no_except(es, index='gitlab_enriched_*', name='ocean_tickets')
logging.warning('Default indices added')
