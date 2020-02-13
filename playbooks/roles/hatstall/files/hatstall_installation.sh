INSTALLATION_DIR="/hatstall-installation"
mkdir -p $INSTALLATION_DIR

cd $INSTALLATION_DIR
git clone https://github.com/chaoss/grimoirelab-sortinghat sortinghat
cd sortinghat/
python -m pip install .

cd $INSTALLATION_DIR
git clone https://github.com/chaoss/grimoirelab-hatstall hatstall
cd hatstall/django-hatstall
python -m pip install .

