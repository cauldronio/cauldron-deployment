# Update Cauldron panels

This guide is for modifying the panels in Kibana, export them and make them available for importing later.

You will need an instance of Cauldron running with all its components up and full access to the containers.

## Steps

1. **Download and install Archimedes from Bitergia**

    Clone Bitergia/archimedes repository from GitHub
    ```
    $ git clone https://github.com/Bitergia/archimedes
    ```
    Create a new Python virtual environment and install archimedes
    ```
    $ python3 -m venv archimedes-env
    $ source archimedes-env/bin/activate
    (archimedes-env) $ pip install -e archimedes
    ```

2. **Create a dashboard**
    
    When you create a new dashboard in Cauldron, a new user and a `.kibana` index are created in Elasticsearch.

    The name for the user will be `dashboardXYZ`, where `XYZ` is the id of the dashboard, and the name for the index will be `.kibana_<hash>_dashboardXYZ`.  
    
    The ID for a dashboard can be easily obtained from the name automatically generated, eg. for Dashboard 20 the id is 20.


3. **Add data**
    
    Once you have created your dashboard, it is important to include data in order to visualize the results.
    
    You have to remember the ID of the dashboards inside Kibana you have modified. You can look at the URL and you can see something like:
    `https://alpha.cauldron.io/kibana/app/kibana#/dashboard/`**4434c9a0-18dd-11e9-ba47-d5cbef43f8d3**`?_g=(...`. You need to copy the bold text.
    If you don't remember what have you modified but you know what you are doing, you can get all the dashboards IDs.


3. **Open Kibana and make your changes**
    
    Open Kibana from Cauldron and make the changes you think are necessary. 
    
    All your modifications will be added to the `.kibana` of that dashboard. If you open a different dashboard, you won't be able to see the changes.

    
4. **Get the password for that dashboard**
    
    For this step you will need to have access to the database and get the password for the specified dashboard (remember to change `XYZ` with the ID of your dashboard): 
    ```
    $ docker exec -ti db_cauldron_service mysql db_cauldron
    > SELECT password FROM CauldronApp_esuser WHERE name='dashboardXYZ';
    ```

5. **Export the changes with Archimedes**
    
    You need to know the ID of the dashboards that have been modified from step 3 and execute the following command inside the archimedes environment.
    ```
    archimedes https://dashboardXYZ:password@HOST:PORT/kibana /tmp/custom-panels --export --obj-type dashboard --obj-id DASHBOARD_ID --force
    ```    
    
    - **dashboardXYZ** is from step 2.
    - **password** is from step 5.
    - **HOST:PORT** is the location where Cauldron is running (localhost:9000 locally).
    - **/tmp/custom-panels** is the location where the dashboards and visualizations will be exported
    - **DASHBOARD_ID** is the dashboard ID obtained from step 3
    
6. **Import panels for the next time**
    
    You can import the panels with Archimedes, but I recommend to include the panels in the deployment directory and test them from scratch.
    
    You have to copy-paste the files generated in **/tmp/custom-panels** (or wherever you stored them) in deployment/docker-panels/archimedes_panels
    
    After that import them the way it has to be:
    - In `aioli` you need to stop the cauldron, delete the panels image, generate it from your local directory and run all the cauldron from 0.
      
