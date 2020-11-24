import os
import django
import logging
from django.core.serializers.json import Serializer as JSONSerializer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Cauldron2.settings")
django.setup()


from CauldronApp import models as cauldron_models
from poolsched import models as poolsched_models
from django.contrib.auth.models import User


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('export')
logger.setLevel(level=logging.INFO)

# EXPORT ALSO DJANGO TABLES

MODELS_EXPORT = [
    cauldron_models.Project,
    cauldron_models.ProjectRole,
    cauldron_models.Repository,
    cauldron_models.GitRepository,
    cauldron_models.GitHubRepository,
    cauldron_models.GitLabRepository,
    cauldron_models.MeetupRepository,
    cauldron_models.AnonymousUser,
    cauldron_models.UserWorkspace,
    cauldron_models.GithubUser,
    cauldron_models.GitlabUser,
    cauldron_models.MeetupUser,
    cauldron_models.SHTask,
    User,
    poolsched_models.Intention,
    poolsched_models.ArchJob,
    poolsched_models.ArchivedIntention,
    poolsched_models.Job,
    poolsched_models.Worker,
    poolsched_models.GitRepo,
    poolsched_models.IGitRaw,
    poolsched_models.IGitEnrich,
    poolsched_models.IGitRawArchived,
    poolsched_models.IGitEnrichArchived,
    poolsched_models.GHRepo,
    poolsched_models.GHToken,
    poolsched_models.IGHRaw,
    poolsched_models.IGHEnrich,
    poolsched_models.IGHRawArchived,
    poolsched_models.IGHEnrichArchived,
    poolsched_models.GHInstance,
    poolsched_models.GLRepo,
    poolsched_models.GLToken,
    poolsched_models.IGLRaw,
    poolsched_models.IGLEnrich,
    poolsched_models.IGLRawArchived,
    poolsched_models.IGLEnrichArchived,
    poolsched_models.GLInstance,
    poolsched_models.MeetupRepo,
    poolsched_models.MeetupToken,
    poolsched_models.IMeetupRaw,
    poolsched_models.IMeetupEnrich,
    poolsched_models.IMeetupRawArchived,
    poolsched_models.IMeetupEnrichArchived,
    poolsched_models.jobs.Log
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
