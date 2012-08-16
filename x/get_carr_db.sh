#!/bin/bash
#
# db backup
# 
#To see output of this script, uncomment the following line:
set -x
ssh pusher@dolph.ccnmtl.columbia.edu "/home/pusher/dump_carr.sh"
scp dolph.ccnmtl.columbia.edu:/tmp/carr.sql .
dropdb carr
createdb -O eddie  carr
psql eddie -d carr -f ./carr.sql
