#!/bin/sh

ENV_PROPERTIES_PATH=
APP_PROPERTIES_PATH=

docker run --name wls -d -p 7001:7001 -v ${CONTAINER_PROPERTIES_PATH}:/u01/oracle/properties -v ${APP_PROPERTIES_PATH}:/u01/oracle/app_config  appello/weblogic
