#!/bin/bash

#ln -s /usr/local/etc/init.d/couchdb /etc/init.d/couchdb
#/etc/init.d/couchdb start
#update-rc.d couchdb defaults

couchdb -b
wget -qO - --retry-connrefused http://127.0.0.1:5984/ | cat


./newUser.py 

