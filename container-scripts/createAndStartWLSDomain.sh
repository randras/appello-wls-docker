#!/bin/bash
#
#Copyright (c) 2014-2018 Oracle and/or its affiliates. All rights reserved.
#
#Licensed under the Universal Permissive License v 1.0 as shown at http://oss.oracle.com/licenses/upl.

#Define DOMAIN_HOME
export DOMAIN_HOME=/u01/oracle/user_projects/domains/$DOMAIN_NAME
echo "Domain Home is: " $DOMAIN_HOME

# If AdminServer.log does not exists, container is starting for 1st time
# So it should start NM and also associate with AdminServer
# Otherwise, only start NM (container restarted)
########### SIGTERM handler ############
function _term() {
   echo "Stopping container."
   echo "SIGTERM received, shutting down the server!"
   ${DOMAIN_HOME}/bin/stopWebLogic.sh
}

########### SIGKILL handler ############
function _kill() {
   echo "SIGKILL received, shutting down the server!"
   kill -9 $childPID
}

# Set SIGTERM handler
trap _term SIGTERM

# Set SIGKILL handler
trap _kill SIGKILL

mkdir -p $ORACLE_HOME/properties
# Create Domain only if 1st execution


PROPERTIES_FILE=/u01/oracle/properties/domain.properties
if [[ ! -e "$PROPERTIES_FILE" ]]; then
   echo "A properties file with the username and password needs to be supplied."
   exit
fi


# Create an empty domain
wlst.sh -skipWLSModuleScanning -loadProperties $PROPERTIES_FILE  /u01/oracle/create-wls-domain.py

# Start Admin Server and tail the logs
${DOMAIN_HOME}/bin/setDomainEnv.sh   
nohup ${DOMAIN_HOME}/startWebLogic.sh &

/u01/oracle/waitForAdminServer.sh


echo "##################### User creation started ##########################"
wlst.sh /u01/oracle/create-users.py /u01/oracle/properties/users.properties

/u01/oracle/createServer.sh

${DOMAIN_HOME}/bin/stopWebLogic.sh

echo "##################### DS creation started ##########################"
wlst.sh -loadProperties /u01/oracle/properties/datasource.properties /u01/oracle/ds-deploy.py
echo "##################### JMS creation started ##########################"
wlst.sh /u01/oracle/jms-deploy.py


nohup ${DOMAIN_HOME}/startWebLogic.sh &

touch ${DOMAIN_HOME}/servers/AdminServer/logs/AdminServer.log
tail -f ${DOMAIN_HOME}/servers/AdminServer/logs/AdminServer.log &

childPID=$!
wait $childPID
