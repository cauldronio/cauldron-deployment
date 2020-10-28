"""
Migrate Opendistro from 0.9 to 1.2.
The Opendistro security index is deleted, this script recreates it from
the Cauldron database
"""
import os
import django
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)-8s - %(message)s')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Cauldron2.settings")
django.setup()


from CauldronApp.models import Dashboard, ESUser
from CauldronApp.opendistro_utils import OpendistroApi
from CauldronApp.views import update_role_dashboard, ES_IN_URL, ES_ADMIN_PSW

for dashboard in Dashboard.objects.all():
    logging.info("=== Dashboard %d ===", dashboard.id)
    users = ESUser.objects.filter(dashboard=dashboard)
    priv = users.get(private=True)
    pub = users.get(private=False)
    logging.info("Users: %s and %s", priv.name, pub.name)

    odfe_api = OpendistroApi(ES_IN_URL, ES_ADMIN_PSW)
    odfe_api.create_user(priv.name, priv.password)
    odfe_api.create_user(pub.name, pub.password)
    odfe_api.put_role(priv.role)
    odfe_api.create_mapping([priv.name, pub.name], priv.role)

    update_role_dashboard(priv.role, dashboard)
