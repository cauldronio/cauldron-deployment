Migrate to Wakame
==========

This migrations scripts only moves the objects from one application to another one. It works similarly to the previous migration scripts.

You may need to export other databases from the old Cauldron and import in the new database like `db_matomo` or `db_sortinghat`  

For this guide it is important to know how Cauldron works, and how it is deployed. If you don't know how to do it, ask or open a new issue.

## Backup SQL data

First, we need to create a dump of the old database:
```
docker exec db_cauldron_service mysqldump -pYOURDBPASSWORD --databases db_cauldron > db_cauldron_old_`date -u +\%Y\%m\%dt\%H\%M\%S.sql`
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
    $ docker cp cauldron_service:/code/Cauldron2/raw_models .
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
