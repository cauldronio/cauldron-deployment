import logging

from cauldron_apps.cauldron.models import GitRepository, GitHubRepository, GitLabRepository, \
    StackExchangeRepository, MeetupRepository
from cauldron_apps.poolsched_git.models import IGitEnrichArchived
from cauldron_apps.poolsched_github.models import IGHEnrichArchived
from cauldron_apps.poolsched_gitlab.models import IGLEnrichArchived
from cauldron_apps.poolsched_meetup.models import IMeetupEnrichArchived
from cauldron_apps.poolsched_stackexchange.models import IStackExchangeEnrichArchived

logger = logging.getLogger(__name__)

logger.info('Migrating Git Repositories')
for repo in GitRepository.objects.all():
    try:
        date = IGitEnrichArchived.objects.filter(repo=repo.repo_sched).latest('completed').completed
    except IGitEnrichArchived.DoesNotExist:
        date = None
    repo.last_refresh = date
    repo.save()

logger.info('Migrating GitHub Repositories')
for repo in GitHubRepository.objects.all():
    try:
        date = IGHEnrichArchived.objects.filter(repo=repo.repo_sched).latest('completed').completed
    except IGHEnrichArchived.DoesNotExist:
        date = None
    repo.last_refresh = date
    repo.save()

logger.info('Migrating GitLab Repositories')
for repo in GitLabRepository.objects.all():
    try:
        date = IGLEnrichArchived.objects.filter(repo=repo.repo_sched).latest('completed').completed
    except IGLEnrichArchived.DoesNotExist:
        date = None
    repo.last_refresh = date
    repo.save()

logger.info('Migrating Meetup Repositories')
for repo in MeetupRepository.objects.all():
    try:
        date = IMeetupEnrichArchived.objects.filter(repo=repo.repo_sched).latest('completed').completed
    except IMeetupEnrichArchived.DoesNotExist:
        date = None
    repo.last_refresh = date
    repo.save()

logger.warning('Migrating StackExchange Repositories')
for repo in StackExchangeRepository.objects.all():
    try:
        date = IStackExchangeEnrichArchived.objects.filter(question_tag=repo.repo_sched).latest('completed').completed
    except IStackExchangeEnrichArchived.DoesNotExist:
        date = None
    repo.last_refresh = date
    repo.save()
