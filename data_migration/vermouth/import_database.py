import os
import logging
import django
import json
import argparse

from django.core import serializers
from django.db import transaction

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Cauldron2.settings")
django.setup()


@transaction.atomic
def import_user(directory):
    path = os.path.join(directory, "User.json")
    logger.info(f'Importing User from {path} ...')
    with open(path, 'r') as data:
        for obj in serializers.deserialize("json", data):
            obj.save()


@transaction.atomic
def import_anonymous_user(directory):
    path = os.path.join(directory, "AnonymousUser.json")
    logger.info(f'Importing AnonymousUser from {path} ...')
    with open(path, 'r') as data:
        for obj in serializers.deserialize("json", data):
            obj.save()


@transaction.atomic
def import_user_workspace(directory):
    path = os.path.join(directory, "UserWorkspace.json")
    logger.info(f'Importing UserWorkspace from {path} ...')
    with open(path, 'r') as data:
        for obj in serializers.deserialize("json", data):
            obj.save()


def import_tokens(directory):
    from poolsched.models import GHToken, GLToken, MeetupToken
    path = os.path.join(directory, "Token.json")
    logger.info(f'Importing Token from {path} ...')
    """
    {
      "model": "CauldronApp.token",
      "pk": 1,
      "fields": {
        "backend": "github",
        "key": "xxx",
        "rate_time": "2020-10-26T00:00:00.000Z",
        "user": 1
      }
    }
    """
    with open(path, 'r') as data:
        objects = json.load(data)
        tokens = []
        for obj in objects:
            fields = obj['fields']
            if fields['backend'] == 'github':
                tokens.append(GHToken(token=fields['key'], user_id=fields['user']))
            elif fields['backend'] == 'gitlab':
                tokens.append(GLToken(token=fields['key'], user_id=fields['user']))
            elif fields['backend'] == 'meetup':
                tokens.append(MeetupToken(token=fields['key'], user_id=fields['user']))
            else:
                logging.error(f"{fields['backend']} not found")
    logger.info(f'Saving tokens ...')
    with transaction.atomic():
        for token in tokens:
            token.save()


def import_projects(directory):
    from CauldronApp.models import Project
    path = os.path.join(directory, "Dashboard.json")
    logger.info(f'Importing Project from {path} ...')
    """
    {
        "model":"CauldronApp.dashboard",
        "pk":1,
        "fields":{
            "created":"2020-10-23T13:16:51.353Z",
            "modified":"2020-10-23T13:16:51.354Z",
            "name":"Project 1",
            "creator":2
        }
    }
    """
    with open(path, 'r') as data:
        objects = json.load(data)
        projects = []
        for obj in objects:
            fields = obj['fields']
            projects.append(
                Project(id=obj['pk'], name=fields['name'], creator_id=fields['creator'])
            )
        logger.info(f'Saving projects ...')
        with transaction.atomic():
            for project in projects:
                project.save()
        # Update created date because by default it is auto_add
        for obj in objects:
            Project.objects.filter(id=obj['pk']).update(created=obj['fields']['created'])



def import_project_role(directory):
    from CauldronApp.models import ProjectRole
    path = os.path.join(directory, "ProjectRole.json")
    logger.info(f'Importing ProjectRole from {path} ...')
    """
    {
        "model":"CauldronApp.projectrole",
        "pk":1,
        "fields":{
            "role":"role_project_22",
            "backend_role":"br_project_22",
            "dashboard":22
        }
    }
    """
    with open(path, 'r') as data:
        objects = json.load(data)
        project_roles = []
        for obj in objects:
            fields = obj['fields']
            project_roles.append(
                ProjectRole(role=fields['role'], backend_role=fields['backend_role'], project_id=fields['dashboard'])
            )
    logger.info(f'Saving project roles ...')
    with transaction.atomic():
        for project in project_roles:
            project.save()


def import_github_user(directory):
    from CauldronApp.models import GithubUser
    path = os.path.join(directory, "GithubUser.json")
    logger.info(f'Importing GithubUser from {path} ...')
    """
    {
        "model":"CauldronApp.githubuser",
        "pk":1,
        "fields":{
            "user":2,
            "username":"pepe",
            "token":3,
            "photo":"url"
        }
    }
    """
    with open(path, 'r') as data:
        objects = json.load(data)
        users = []
        for obj in objects:
            fields = obj['fields']
            users.append(
                GithubUser(user_id=fields['user'], username=fields['username'], photo=fields['photo'])
            )
    logger.info(f'Saving GithubUsers  ...')
    with transaction.atomic():
        for u in users:
            u.save()


def import_gitlab_user(directory):
    from CauldronApp.models import GitlabUser
    path = os.path.join(directory, "GitlabUser.json")
    logger.info(f'Importing GitlabUser from {path} ...')
    """
    {
        "model":"CauldronApp.gitlabuser",
        "pk":12,
        "fields":{
            "user":1,
            "username":"pepe",
            "token":2,
            "photo":"url"
        }
    }
    """
    with open(path, 'r') as data:
        objects = json.load(data)
        users = []
        for obj in objects:
            fields = obj['fields']
            users.append(
                GitlabUser(user_id=fields['user'], username=fields['username'], photo=fields['photo'])
            )
    logger.info(f'Saving GitlabUser  ...')
    with transaction.atomic():
        for u in users:
            u.save()


def import_meetup_user(directory):
    from CauldronApp.models import MeetupUser
    path = os.path.join(directory, "MeetupUser.json")
    logger.info(f'Importing MeetupUser from {path} ...')
    """
    {
        "model":"CauldronApp.meetupuser",
        "pk":12,
        "fields":{
            "user":1,
            "username":"pepe",
            "token":2,
            "photo":"url"
        }
    }
    """
    with open(path, 'r') as data:
        objects = json.load(data)
        users = []
        for obj in objects:
            fields = obj['fields']
            users.append(
                MeetupUser(user_id=fields['user'], username=fields['username'], photo=fields['photo'])
            )
    logger.info(f'Saving MeetupUser  ...')
    with transaction.atomic():
        for u in users:
            u.save()


def import_repositories(directory):
    from CauldronApp.models import GitRepository, GitHubRepository, GitLabRepository, MeetupRepository
    from CauldronApp import datasources
    path = os.path.join(directory, "Repository.json")
    logger.info(f'Importing Repository from {path} ...')
    """
    {
        "model":"CauldronApp.repository",
        "pk":1,
        "fields":{
            "url":"https://github.com/owner/repo",
            "backend":"github",
            "dashboards":[
                1,
                2
            ]
        }
    }
    """
    with open(path, 'r') as data:
        objects = json.load(data)
        total = len(objects)
        progress = total // 50 or 1
        for i, obj in enumerate(objects):
            if i % progress == 0:
                logger.info(f"{i}/{total}")
            fields = obj['fields']
            if fields['backend'] == 'git':
                git = GitRepository(url=fields['url'])
                try:
                    git.save()
                except django.db.utils.IntegrityError:
                    logger.error(f"Duplicated: Git({fields['url']})")
                    continue
                if fields['dashboards']:
                    git.projects.add(*fields['dashboards'])
                git.link_sched_repo()
            elif fields['backend'] == 'github':
                owner, repo = datasources.github.parse_input_data(fields['url'])
                if not owner or not repo:
                    logger.error(f"Error parsing {fields['url']}")
                    continue
                gh = GitHubRepository(owner=owner, repo=repo)
                try:
                    gh.save()
                except django.db.utils.IntegrityError:
                    logger.error(f"Duplicated: GitHub({fields['url']})")
                    continue
                if fields['dashboards']:
                    gh.projects.add(*fields['dashboards'])
                gh.link_sched_repo()
            elif fields['backend'] == 'gitlab':
                url_parsed = fields['url'].split('/')
                owner = url_parsed[-2]
                repo = url_parsed[-1]
                if not owner or not repo:
                    logger.error(f"Error parsing {fields['url']}")
                    continue
                gl = GitLabRepository(owner=owner, repo=repo)
                try:
                    gl.save()
                except django.db.utils.IntegrityError:
                    logger.error(f"Duplicated: GitLab({fields['url']})")
                    continue
                if fields['dashboards']:
                    gl.projects.add(*fields['dashboards'])
                gl.link_sched_repo()
            elif fields['backend'] == 'meetup':
                meet = MeetupRepository(group=fields['url'])
                try:
                    meet.save()
                except django.db.utils.IntegrityError:
                    logger.error(f"Duplicated: Meetup({fields['url']})")
                    continue
                if fields['dashboards']:
                    meet.projects.add(*fields['dashboards'])
                meet.link_sched_repo()
            else:
                logging.error(f"{fields} not found")


def configure_parser():
    parser = argparse.ArgumentParser(description='Import tables exported from Cauldron Udon.')
    parser.add_argument('location', type=str,
                        help='directory of models in json format')
    return parser


if __name__ == '__main__':
    parser = configure_parser()
    args = parser.parse_args()
    input_dir = args.location
    import_user(input_dir)
    import_anonymous_user(input_dir)
    import_user_workspace(input_dir)
    import_tokens(input_dir)
    import_projects(input_dir)
    import_project_role(input_dir)
    import_github_user(input_dir)
    import_gitlab_user(input_dir)
    import_meetup_user(input_dir)
    import_repositories(input_dir)
