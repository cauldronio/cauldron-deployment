import os
import django
import logging
from django.core.serializers.json import Serializer as JSONSerializer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Cauldron2.settings")
django.setup()

from CauldronApp import models
from django.contrib.auth.models import User


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('export')

# EXPORT ALSO DJANGO TABLES

MODELS_EXPORT = [
    models.AnonymousUser,
    models.UserWorkspace,
    models.Token,
    models.Repository,
    models.GithubUser,
    models.GitlabUser,
    models.MeetupUser,
    models.Dashboard,
    models.ProjectRole,
    User
]


def export(model, location):
    json_serializer = JSONSerializer()
    with open(location, "w") as out:
        json_serializer.serialize(model.objects.all(), stream=out)


if __name__ == '__main__':
    output_dir = 'raw_models'
    try:
        os.mkdir(output_dir)
    except FileExistsError:
        pass

    for model_class in MODELS_EXPORT:
        path = os.path.join(output_dir, f"{model_class.__name__}.json")
        logger.info(f'Exporting {model_class} at {path} ...')
        export(model_class, path)
