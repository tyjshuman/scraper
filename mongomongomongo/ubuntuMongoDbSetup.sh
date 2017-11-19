#!/bin/bash

#import public key
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
#Create source list file 
echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
#Update
sudo apt-get update
#install mongo
sudo apt-get install -y mongodb-org

#Create new mongo service file
cat <<EOF > /lib/systemd/system/mongod.service
[Unit]
Description=High-performance, schema-free document-oriented database
After=network.target
Documentation=https://docs.mongodb.org/manual

[Service]
User=mongodb
Group=mongodb
ExecStart=/usr/bin/mongod --quiet --config /etc/mongod.conf

[Install]
WantedBy=multi-user.target
EOF

#Reload service, start mongod and enable that sucker
sudo systemctl daemon-reload
sudo systemctl start mongod
sudo systemctl enable mongod
#Check that mongod is listening on port 27017
netstat -plntu | grep mongod

#install pymongo and simple-json
sudo pip install pymongo
sudo pip install simple-json
