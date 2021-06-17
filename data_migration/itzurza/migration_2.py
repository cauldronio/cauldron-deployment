from CauldronApp.models import GitRepository, GitHubRepository, GitLabRepository
from cauldron_apps.poolsched_git.models import IGitEnrich
from cauldron_apps.poolsched_github.models import IGHEnrich
from cauldron_apps.poolsched_gitlab.models import IGLEnrich

import urllib3
urllib3.disable_warnings()


for r in GitRepository.objects.all():
    if not r.repo_sched:
        print(r)
        continue
    IGitEnrich(repo=r.repo_sched).update_db_metrics()

for r in GitHubRepository.objects.all():
    if not r.repo_sched:
        print(r)
        continue
    IGHEnrich(repo=r.repo_sched).update_db_metrics()

for r in GitLabRepository.objects.all():
    if not r.repo_sched:
        print(r)
        continue
    IGLEnrich(repo=r.repo_sched).update_db_metrics()
