"""
Description:
    New indices have been added (gitlab merges and github2) and git aoc has been removed

    This script updates the roles for each dashboard with new permissions and
    import the new index patterns and update the visualizations in the workspaces.

How to:
    docker cp data_migration/iceberg-01-update-panels.py cauldron_service:/code/Cauldron2/
    docker exec cauldron_service python Cauldron2/iceberg-01-update-panels.py
"""
import os
import django
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)-8s - %(message)s')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Cauldron2.settings")
django.setup()


from CauldronApp import views, models, kibana_objects
from Cauldron2 import settings

# Import new panels from Global to custom workspaces
obj = kibana_objects.export_all_objects(views.KIB_IN_URL, settings.ES_ADMIN_PSW, "global")
num_tenants = models.UserWorkspace.objects.count()
for i, tenant_name in enumerate(models.UserWorkspace.objects.values_list('tenant_name', flat=True)):
    logging.info(f"{i}/{num_tenants} - {tenant_name}")
    kibana_objects.import_object(views.KIB_IN_URL, settings.ES_ADMIN_PSW, obj, tenant_name)

# Update role for each dashboard
num_dashboards = models.Dashboard.objects.count()
for i, dash in enumerate(models.Dashboard.objects.all().select_related('projectrole')):
    logging.info(f"{i}/{num_dashboards} - {dash.id}")
    views.update_role_dashboard(dash.projectrole.role, dash)
