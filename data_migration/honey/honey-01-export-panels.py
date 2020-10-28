import requests
from CauldronApp import models


def export_all_objects(kibana_url, user, password):
    """
    This method export all the object from the defined tenant using saved_objects API and returns the contents
    :return:
    """
    headers = {'kbn-xsrf': 'true',
               'securitytenant': 'private'}
    data = {
        "type": ["index-pattern", "visualization", "dashboard", "search", "config", "query", "url"],
        "includeReferencesDeep": True
    }
    saved_objects_api = "{}/api/saved_objects/_export".format(kibana_url)
    r = requests.post(saved_objects_api,
                      auth=(user, password),
                      data=data,
                      verify=False,
                      headers=headers)
    if r.ok:
        with open('dashboards/{}.ndjson'.format(user), 'wb') as f:
            f.write(r.content)
    else:
        print("error in {}".format(user))


for u in models.ESUser.objects.filter(private=True):
    print(u.name)
    export_all_objects('https://cauldron.io/kibana', u.name, u.password)
