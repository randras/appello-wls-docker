#!/bin/bash

MS_NAME=$1

echo "MS_NAME: $MS_NAME"

echo "Server $MS_NAME is going to be stopped!!"

/u01/oracle/user_projects/domains/base_domain/bin/stopManagedWebLogic.sh $MS_NAME localhost:7001 $ADMIN_USERNAME $ADMIN_PASSWORD

echo "Servers STOPPED!!"

wlst.sh manageApplication.py -u $ADMIN_USERNAME -p $ADMIN_PASSWORD -a localhost:7001 -n khcollateral-$MS_NAME-ear -f /app_deploy/khcollateral-ear.ear -t $MS_NAME

echo "Server start $MS_NAME"

wlst.sh start-server.py
