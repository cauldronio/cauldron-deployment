"""
With this script we can group about 95% of Git repositories with GitHub and GitLab repositories
"""

from urllib.parse import unquote

from CauldronApp.models import GitRepository, GitHubRepository, GitLabRepository
from CauldronApp.datasources import github
from cauldron_apps.cauldron.models import RepositoryMetrics


for r in GitHubRepository.objects.all():
    metrics_name = f'GitHub {r.owner}/{r.repo}'
    metrics, _ = RepositoryMetrics.objects.get_or_create(name=metrics_name)
    git_url = f'https://github.com/{r.owner}/{r.repo}.git'
    r.metrics = metrics
    r.save()
    gitrepo = GitRepository.objects.filter(url=git_url).first()
    if gitrepo:
        gitrepo.metrics = metrics
        gitrepo.save()

for r in GitLabRepository.objects.all():
    metrics_name = f'{r.instance.name} {r.owner}/{r.repo}'
    metrics, _ = RepositoryMetrics.objects.get_or_create(name=metrics_name)
    git_url = f'{r.instance.endpoint}/{r.owner}/{r.repo}.git'
    r.metrics = metrics
    r.save()
    gitrepo = GitRepository.objects.filter(url=unquote(git_url)).first()
    if gitrepo:
        gitrepo.metrics = metrics
        gitrepo.save()

for r in GitRepository.objects.filter(metrics=None).all():
    owner, repo = github.parse_input_data(r.url)
    if owner and repo:
        metrics_name = f'GitHub {owner}/{repo}'
        metrics, _ = RepositoryMetrics.objects.get_or_create(name=metrics_name)
        r.metrics = metrics
        r.save()
    else:
        metrics_name = f'Git {r.url}'
        metrics, _ = RepositoryMetrics.objects.get_or_create(name=metrics_name)
        r.metrics = metrics
        r.save()
