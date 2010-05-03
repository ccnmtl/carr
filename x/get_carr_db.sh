#!/bin/bash

#
# db backup
# 

#To see output of this script, uncomment the following line:
#set -x

############
DB_BACKUPS=~
PREFIX=carr_prod_
DATE=$PREFIX`date +"%F_%R" | sed 's/-/_/g' | sed 's/:/_/g'`
#PROD_SERVER_HOSTNAME=worth.ccnmtl.columbia.edu
PROD_SERVER_HOSTNAME=kodos.ccnmtl.columbia.edu

############


#Note: this assumes there is a POSTGRES user on the prod server with your username, with read permission to all the tables in the database. You might need to run:
# sudo -u postgres createuser -D -A -P eddie
# worth=# grant all on database worth to eddie;
# worth=# grant all on table auth_group to eddie; -- and so on, for every single table in the database.

echo "OK. We are downloading the database from $PROD_SERVER_HOSTNAME."
echo "File will be backed up in: $DB_BACKUPS/$DATE"
ssh $PROD_SERVER_HOSTNAME "sudo -u pusher pg_dump carr >  $DB_BACKUPS/$DATE.out"
echo "Fetching file to your backup directory, $DB_BACKUPS."
scp $PROD_SERVER_HOSTNAME:$DATE.out $DB_BACKUPS
echo "Dropping local database carr"
sudo -u postgres psql -Upostgres -c 'drop database carr'
echo "Creating database on dev machine."
sudo -u postgres createdb -O postgres carr
echo "Adding data to the new database."
sudo -u postgres psql -Upostgres -d carr -f $DB_BACKUPS/$DATE.out

#echo "OK, done making new database $DATE. Now changing your settings to point at it."
#sed -i "s/worth_prod_...._.._.._.._../worth/g" ./settings_shared.py

#echo "Other settings files you might want to update are:"
#locate settings_shared.py | grep worth | grep -v 'pyc\|_in\|~'
