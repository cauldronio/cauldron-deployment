"""
The Opendistro security index is deleted, this script recreates it from
the Cauldron database
"""
import os
import django
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)-8s - %(message)s')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Cauldron2.settings")
django.setup()


from CauldronApp.models import Dashboard
from CauldronApp import views

for dashboard in Dashboard.objects.all():
    logging.info("=== Dashboard %d ===", dashboard.id)
    views.create_project_elastic_role(dashboard)
    views.update_role_dashboard(dashboard.projectrole.role, dashboard)
