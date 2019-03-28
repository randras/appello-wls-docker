
FROM  store/oracle/weblogic:12.2.1.3-dev

ARG CUSTOM_DOMAIN_NAME="${CUSTOM_DOMAIN_NAME:-base_domain}" 

# WLS Configuration
# ---------------------------
ENV DOMAIN_NAME="${CUSTOM_DOMAIN_NAME}" \
    PRE_DOMAIN_HOME=/u01/oracle/user_projects \
    ADMIN_HOST="localhost" \
    NM_PORT="5556" \
    MS_PORT="7004" \
    DEBUG_PORT="8453" \
    ORACLE_HOME=/u01/oracle \
    SCRIPT_FILE=/u01/oracle/createAndStartWLSDomain.sh \
    CONFIG_JVM_ARGS="-Dweblogic.security.SSL.ignoreHostnameVerification=true"  \
    DOMAIN_HOME="/u01/oracle/user_projects/domains/${DOMAIN_NAME}" \ 
    PATH=$PATH:/u01/oracle/oracle_common/common/bin:/u01/oracle/wlserver/common/bin:${DOMAIN_HOME}:${DOMAIN_HOME}/bin:/u01/oracle

# Domain and Server environment variables
# ------------------------------------------------------------
ENV ADMIN_PORT="${ADMIN_PORT:-7001}"  \
    ADMIN_USERNAME="${ADMIN_USERNAME:-weblogic}" \
    ADMIN_NAME="${ADMIN_NAME:-AdminServer}" \
    MS_NAME="${MS_NAME:-"KHC"}" \
    NM_NAME="${NM_NAME:-"Machine-localhost"}" \
    ADMIN_PASSWORD="${ADMIN_PASSWORD:-"legoland1"}" \
    CLUSTER_NAME="${CLUSTER_NAME:-DockerCluster}" \
    DEBUG_FLAG=true \
    PRODUCTION_MODE=dev

# Add files required to build this image
COPY container-scripts/* /u01/oracle/

#Create directory where domain will be written to
USER root
RUN chmod +xw /u01/oracle/*.sh && \
    chmod +xw /u01/oracle/*.py && \
    mkdir -p $PRE_DOMAIN_HOME && \
    chown -R oracle:oracle $PRE_DOMAIN_HOME && \
    chmod -R a+xwr $PRE_DOMAIN_HOME && \ 
    mkdir -p $DOMAIN_HOME && \
    chmod -R a+xwr $DOMAIN_HOME && \
    mkdir -p /app_deploy


VOLUME $PRE_DOMAIN_HOME
# Expose Node Manager default port, and also default for admin and managed server
EXPOSE $NM_PORT $ADMIN_PORT $MS_PORT $DEBUG_PORT

USER root
WORKDIR $ORACLE_HOME

CMD "/u01/oracle/createAndStartWLSDomain.sh" 




