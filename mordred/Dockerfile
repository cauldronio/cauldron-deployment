# The container produced with this file contains all GrimoireLab libraries and executables.
# It is configured for getting repositories from a database and running mordred

FROM grimoirelab/installed:0.2.26
MAINTAINER Jose J Merchante <jjmerchante@bitergia.com>

ENV MORDRED_DIR /code

USER root

# Install package for mysql + python
RUN apt-get update && apt-get install -y default-libmysqlclient-dev

# Download Mordred code
WORKDIR ${MORDRED_DIR}
RUN git clone https://gitlab.com/cauldron2/mordred.git --depth 1

# Install requirements
WORKDIR ${MORDRED_DIR}/mordred
RUN pip install -q -r requirements.txt

WORKDIR ${MORDRED_DIR}/mordred/MordredManager/

VOLUME ["/dashboard_logs"]

ENTRYPOINT ["python3",  "manager.py"]
