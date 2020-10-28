Migrate to Cauldron 1.0
==========
The models between the old and the new Cauldron have changed. Some of them have been removed and others have been updated. In this document, we explain how the migration script works for only the webserver database.

You may need to export other databases from the old Cauldron and import in the new database like `db_matomo` or `db_sortinghat`  

For this guide it is important to know how Cauldron works, and how it is deployed. If you don't know how to do it, ask or open a new issue.

## Backup SQL data

First, we need to create a dump of the old database:
```
docker exec db_cauldron_service mysqldump --databases db_cauldron > db_cauldron_old_`date -u +\%Y\%m\%dt\%H\%M\%S.sql`
```

## Export models

We have to run `export_database.py`, for that we will have to:

- Kill all the Docker containers except `cauldron_service` and `db_cauldron`.

- Copy the migration script `export_database.py` inside `cauldron_service` container to `cauldron-web/Cauldron2/` 
and execute it. 

    ```
    $ docker cp export_database.py cauldron_service:/code/Cauldron2/
    $ docker exec cauldron_service python /code/Cauldron2/export_database.py
    ```
    It will generate a directory named `raw_models/` with all the objects necessary for the migration. Copy it outside the container:
    ```
    $ docker cp cauldron_service:/code/raw_models .
    ```

## Import models

The new directory created will be used to fill the new database for the new Cauldron.
- We are going to run the new version of Cauldron. It is preferred to run only the webserver and the database, so other components will not be affected:

    ```
    $ ansible-playbook -i inventories/xxx cauldron.yml -t webserver,database
    ``` 

- Copy the directory `raw_models/` previously created inside the container and the script `import_database.py`:
    ```
    $ docker cp raw_models cauldron_service:/code/Cauldron2/
    $ docker cp import_database.py cauldron_service:/code/Cauldron2/
    ```
 
- Execute the script `import_database.py` inside the container. It can take several minutes to finish depending on the size of your database:
    ```
    $ docker exec -ti cauldron_service python Cauldron2/import_database.py /code/Cauldron2/raw_models
    ```

- Run Cauldron normally and check the data is correct:
    ```
    $ ansible-playbook -i inventories/xxx cauldron.yml
    ```

Models exported-imported
===============

Old models:
- `User`: Unchanged
- `AnonymousUser`: Unchanged
- `UserWorkspace`: Unchanged
- `Token`: Removed (new tokens)
- `Repository`: Removed (new repositories)
- `Task`: Removed (NO MIGRATION)
- `CompletedTask`: Removed (NO MIGRATION)
- `SHTask`: Removed (NO MIGRATION)
- `GithubUser`:
    - Remove 'token' Foreign key
- `GitlabUser`:
    - Remove 'token' Foreign key
- `MeetupUser`:
    - Remove 'token' Foreign key
- `Dashboard`:
    - Renamed to Project
    - Remove 'modified' field
- `ProjectRole`:
    - Rename 'dashboard' to 'project'

New models in Cauldron:
- `Repository`:
    - `projects`: ManyToMany: `Project`
    - `backend`: Choices(GIT, GITHUB, GITLAB, MEETUP)

- `GitRepository(Repository)`:
    - `url`: From old repo
    - `repo_sched`: FK: sched.GitRepo

- `GitHubRepository(Repository)`:
    - `owner`: From old repo, parsed
    - `repo`: From old repo, parsed
    - `repo_sched`: FK: sched.GHRepo

- `GitLabRepository(Repository)`:
    - `owner`: From old repo, parsed
    - `repo`: From old repo, parsed
    - `repo_sched`: FK: sched.GLRepo
    
- `MeetupRepository(Repository)`:
    - `group`: From old repo
    - `repo_sched`: FK: sched.MeetupRepo

New models in Poolsched that are created for the migration:
- `GitRepo`:
    - `url`: From old repo
    - `created`: From old repo
    
- `GHRepo`:
    - `owner`: From old repo, parsed
    - `repo`: From old repo, parsed
    - `instance`: All github.com
    - `created`: From old repo
    
- `GLRepo`:
    - `owner`: From old repo, parsed
    - `repo`: From old repo, parsed
    - `instance`: All gitlab.com
    - `created`: From old repo
    
- `MeetupRepo`:
    - `url`: From old repo
    - `created`: From old repo
    
- `GHToken`:
    - `token`: From old (token,github)
    - `reset`: now()
    - `user`: From old token
    - `jobs`: ManyToMany(sched.Job)

- `GLToken`:
    - `token`: From old (token,gitlab)
    - `reset`: now()
    - `user`: From old token
    - `jobs`: ManyToMany(sched.Job)

- `MeetupToken`:
    - `token`: From old (token,meetup)
    - `reset`: now()
    - `user`: From old token
    - `jobs`: ManyToMany(sched.Job)
