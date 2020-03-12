# The container produced with this file contains all GrimoireLab libraries and executables.
# It is configured for getting tasks from a database and running them

FROM cauldronio/grimoirelab:0.2.39.pre

ENV CODE_WORKER /code

USER root

RUN apt-get update && apt-get install -y default-libmysqlclient-dev

# Add code from src folder
WORKDIR ${CODE_WORKER}
ADD src ${CODE_WORKER}

# Install requirements
RUN pip install -q -r requirements.txt

WORKDIR ${CODE_WORKER}/MordredManager/

VOLUME ["/dashboard_logs"]

ENTRYPOINT ["python3",  "manager.py"]
