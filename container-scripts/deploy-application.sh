#!/bin/bash

MS_NAME=$1
APPLICATION_NAME=$2

echo "MS_NAME: $MS_NAME"
echo "MS_NAME: $APPLICATION_NAME"

echo "Server $MS_NAME is going to be stopped!!"

/u01/oracle/user_projects/domains/base_domain/bin/stopManagedWebLogic.sh $MS_NAME $ADMIN_HOST:$ADMIN_PORT $ADMIN_USERNAME $ADMIN_PASSWORD

echo "Servers STOPPED!!"

wlst.sh manageApplication.py -u $ADMIN_USERNAME -p $ADMIN_PASSWORD -a $ADMIN_HOST:$ADMIN_PORT -n $APPLICATION_NAME -f /app_deploy/$APPLICATION_NAME.ear -t $MS_NAME

echo "Server start $MS_NAME"

wlst.sh start-server.py
