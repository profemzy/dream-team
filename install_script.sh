#!/usr/bin/env bash
#!/bin/bash

# install web server dependencies
sudo apt-get update
sudo apt-get -y install python python-virtualenv nginx supervisor

# install application (source location in $1)
mkdir /home/profemzy/python-ibadan
cp -R /home/profemzy/dream-team/* /home/profemzy/python-ibadan/

# create a virtualenv and install dependencies
virtualenv /home/profemzy/python-ibadan/venv
/home/profemzy/python-ibadan/venv/bin/pip install -r /home/profemzy/python-ibadan/requirements.txt

# configure supervisor
sudo cp /profemzy/python-ibadan/python-ibadan.conf /etc/supervisor/conf.d/
sudo mkdir /var/log/python-ibadan
sudo supervisorctl reread
sudo supervisorctl update

# configure nginx
sudo cp /profemzy/python-ibadan/python-ibadan.nginx /etc/nginx/sites-available/python-ibadan
sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/python-ibadan /etc/nginx/sites-enabled/
sudo service nginx restart

echo Application deployed to http://40.68.88.198/
