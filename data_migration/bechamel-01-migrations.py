import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Cauldron2.settings")
django.setup()

from CauldronApp.models import ESUser, Dashboard
from CauldronApp.views import generate_random_uuid, update_role_dashboard, ES_IN_URL, ES_ADMIN_PSW
from CauldronApp.opendistro_utils import OpendistroApi


odfe_api = OpendistroApi(ES_IN_URL, ES_ADMIN_PSW)

for d in Dashboard.objects.all():
    role_name = "roledashboard{}".format(d.id)
    esu_priv = ESUser.objects.get(dashboard=d, private=True)
    esu_priv.role = role_name
    esu_priv.save()

    esu_pub_pass = generate_random_uuid(length=32, delimiter='')
    esu_pub_name = "publicdashboard{}".format(d.id)
    esu_pub = ESUser(name=esu_pub_name, password=esu_pub_pass,
                     role=role_name, dashboard=d, private=False)
    esu_pub.save()

    odfe_api.create_user(esu_priv.name, esu_priv.password)
    odfe_api.create_user(esu_pub.name, esu_pub.password)
    odfe_api.create_role(role_name)
    odfe_api.create_mapping([esu_priv.name, esu_pub.name], role_name)

    update_role_dashboard(role_name, d)

