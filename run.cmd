
set ENV_PROPERTIES_PATH=C:\workspace\appello-wls-docker\properties
set APP_PROPERTIES_PATH=C:\tmp
set DEPLOYMENT_DIR=C:\tmp\deployment

docker run --name wls -d -p 7001:7001 -v "%ENV_PROPERTIES_PATH%":/u01/oracle/properties -v "%APP_PROPERTIES_PATH%":/u01/oracle/app_config -v %DEPLOYMENT_DIR%:/app_deploy appello/weblogic:latest
