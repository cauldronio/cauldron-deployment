import os
import logging
import django
import json
import argparse

from django.db import transaction
from django.core.serializers.python import Deserializer

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Cauldron2.settings")
django.setup()

from cauldron_apps.cauldron import models as cauldron_models
from cauldron_apps.poolsched_github import models as github_models
from cauldron_apps.poolsched_gitlab import models as gitlab_models
from cauldron_apps.poolsched_meetup import models as meetup_models
from cauldron_apps.poolsched_git import models as git_models
from poolsched import models as poolsched_models
from django.contrib.auth.models import User


MODELS_MAP = {
    'User.json': User,
    'Log.json': poolsched_models.jobs.Log,
    'Worker.json': poolsched_models.Worker,
    'AnonymousUser.json': cauldron_models.AnonymousUser,
    'ArchJob.json': poolsched_models.ArchJob,
    'ArchivedIntention.json': poolsched_models.ArchivedIntention,
    'GHInstance.json': github_models.GHInstance,
    'GHRepo.json': github_models.GHRepo,
    'Job.json': poolsched_models.Job,
    'GHToken.json': github_models.GHToken,
    'GLInstance.json': gitlab_models.GLInstance,
    'GLRepo.json': gitlab_models.GLRepo,
    'GLToken.json': gitlab_models.GLToken,
    'Project.json': cauldron_models.Project,
    'Repository.json': cauldron_models.Repository,
    'GitHubRepository.json': cauldron_models.GitHubRepository,
    'GitLabRepository.json': cauldron_models.GitLabRepository,
    'GitRepo.json': git_models.GitRepo,
    'GitRepository.json': cauldron_models.GitRepository,
    'GithubUser.json': cauldron_models.GithubUser,
    'GitlabUser.json': cauldron_models.GitlabUser,
    'Intention.json': poolsched_models.Intention,
    'IGHEnrich.json': github_models.IGHEnrich,
    'IGHEnrichArchived.json': github_models.IGHEnrichArchived,
    'IGHRaw.json': github_models.IGHRaw,
    'IGHRawArchived.json': github_models.IGHRawArchived,
    'IGLEnrich.json': gitlab_models.IGLEnrich,
    'IGLEnrichArchived.json': gitlab_models.IGLEnrichArchived,
    'IGLRaw.json': gitlab_models.IGLRaw,
    'IGLRawArchived.json': gitlab_models.IGLRawArchived,
    'IGitEnrich.json': git_models.IGitEnrich,
    'IGitEnrichArchived.json': git_models.IGitEnrichArchived,
    'IGitRaw.json': git_models.IGitRaw,
    'IGitRawArchived.json': git_models.IGitRawArchived,
    'MeetupRepo.json': meetup_models.MeetupRepo,
    'MeetupRepository.json': cauldron_models.MeetupRepository,
    'MeetupToken.json': meetup_models.MeetupToken,
    'MeetupUser.json': cauldron_models.MeetupUser,
    'IMeetupEnrich.json': meetup_models.IMeetupEnrich,
    'IMeetupEnrichArchived.json': meetup_models.IMeetupEnrichArchived,
    'IMeetupRaw.json': meetup_models.IMeetupRaw,
    'IMeetupRawArchived.json': meetup_models.IMeetupRawArchived,
    'ProjectRole.json': cauldron_models.ProjectRole,
    'SHTask.json': cauldron_models.SHTask,
    'UserWorkspace.json': cauldron_models.UserWorkspace,
}


def configure_parser():
    parser = argparse.ArgumentParser(description='Import tables exported from Vermouth to Wakame.')
    parser.add_argument('location', type=str,
                        help='directory of models in json format')
    return parser


@transaction.atomic
def import_model(model_label, objects):
    for obj in objects:
        obj['model'] = model_label
    for item in Deserializer(objects):
        item.save()


def import_models(directory):
    for file, model in MODELS_MAP.items():
        path = os.path.join(directory, file)
        model_label = model._meta.label
        logger.info(f'Importing {file} ...')
        with open(path, 'r') as data:
            objects = json.load(data)
            import_model(model_label, objects)


if __name__ == '__main__':
    parser = configure_parser()
    args = parser.parse_args()
    input_dir = args.location
    import_models(input_dir)
