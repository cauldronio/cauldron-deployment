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
kib_url_auth = "{}://{}:{}@{}:{}".format(settings.KIB_PROTO,
                                         settings.PANELS_USERNAME,
                                         settings.PANELS_USER_PSW,
                                         settings.KIB_IN_HOST,
                                         settings.KIB_PORT)

archimedes = Archimedes(kib_url_auth, '/panels')
archimedes.import_from_disk(obj_type='dashboard', obj_id='Overview',
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
context = create_ssl_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
es = Elasticsearch([settings.ES_IN_HOST], scheme=settings.ES_PROTO, port=settings.ES_PORT,
                   http_auth=("admin", settings.ES_ADMIN_PSW), ssl_context=context)

es.indices.create('git_enrich_default', ignore=400)
es.indices.create('git_aoc_enriched_default', ignore=400)
es.indices.create('github_enrich_default', ignore=400)
es.indices.create('gitlab_enriched_default', ignore=400)


def put_alias_no_except(es_obj, index, name):
    try:
        es_obj.indices.put_alias(index=index, name=name)
    except NotFoundError:
        pass


put_alias_no_except(es, index='git_aoc_enriched_*', name='git_aoc_enriched')
put_alias_no_except(es, index='git_enrich_*', name='git_enrich')
put_alias_no_except(es, index='github_enrich_*', name='github_enrich')
put_alias_no_except(es, index='gitlab_enriched_*', name='gitlab_enriched')
