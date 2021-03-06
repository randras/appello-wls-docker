#Copyright (c) 2014-2018 Oracle and/or its affiliates. All rights reserved.
#
#Licensed under the Universal Permissive License v 1.0 as shown at http://oss.oracle.com/licenses/upl.
#
# Script to create and add a Managed Server automatically to the domain's AdminServer running on 'wlsadmin'.
#
# Since: October, 2014
# Author: bruno.borges@oracle.com
#
# =============================
import os
import random
import string
import socket

#cluster_name  = os.environ.get("CLUSTER_NAME", "DockerCluster")
ms_port   = int(os.environ.get("MS_PORT", "7004"))

#print('cluster_name     : [%s]' % cluster_name);
print('ms_port          : [%s]' % ms_port);

execfile('/u01/oracle/commonfuncs.py')

# Functions
def randomName():
  return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(6)])


# ManagedServer details
# msinternal = socket.gethostbyname(hostname)
msinternal = ''
msname = os.environ.get('MS_NAME', 'ManagedServer')
nmname = os.environ.get('NM_NAME', 'Machine-' + hostname)
mshost = os.environ.get('MS_HOST', msinternal)
msport = os.environ.get('MS_PORT', ms_port)
mswmargs = os.environ.get('MS_VM_ARGS', '')
memargs = os.environ.get('USER_SERVER_MEM_ARGS', '-Xms512m -Xmx4g -Xss4m -XX:NewSize=256m -XX:MaxNewSize=1g -XX:MaxMetaspaceSize=1g -XX:GCTimeRatio=2 -XX:ParallelGCThreads=8 -XX:+UseParNewGC -XX:SurvivorRatio=8 -XX:+DisableExplicitGC -XX:MaxGCPauseMillis=2000 -XX:+UseStringDeduplication')

print('msname     : [%s]' % msname);
print('nmname     : [%s]' % nmname);
print('mshost     : [%s]' % mshost);
print('msport     : [%s]' % msport);
print('memargs    : [%s]' % memargs);
# Connect to the AdminServer
# ==========================
connectToAdmin()

# Create a ManagedServer
# ======================
editMode()
cd('/')
cmo.createServer(msname)

cd('/Servers/' + msname)
cmo.setMachine(getMBean('/Machines/%s' % nmname))
#cmo.setCluster(getMBean('/Clusters/%s' % cluster_name))

# Default Channel for ManagedServer
# ---------------------------------
cmo.setListenAddress(msinternal)
cmo.setListenPort(int(msport))
cmo.setListenPortEnabled(true)
cmo.setExternalDNSName(mshost)

# Disable SSL for this ManagedServer
# ----------------------------------
cd('/Servers/%s/SSL/%s' % (msname, msname))
cmo.setEnabled(false)

# Custom Channel for ManagedServer
# --------------------------------
#cd('/Servers/' + msname)
#cmo.createNetworkAccessPoint('Channel-0')

#cd('/Servers/' + msname + '/NetworkAccessPoints/Channel-0')
#cmo.setProtocol('t3')
#cmo.setEnabled(true)
#cmo.setPublicAddress(mshost)
#cmo.setPublicPort(int(msport))
#cmo.setListenAddress(msinternal)
#cmo.setListenPort(int(msport))
#cmo.setHttpEnabledForThisProtocol(true)
#cmo.setTunnelingEnabled(false)
#cmo.setOutboundEnabled(false)
#cmo.setTwoWaySSLEnabled(false)
#cmo.setClientCertificateEnforced(false)

# Custom Startup Parameters because NodeManager writes wrong AdminURL in startup.properties
# -----------------------------------------------------------------------------------------
cd('/Servers/%s/ServerStart/%s' % (msname, msname))
arguments = '-Djava.security.egd=file:/dev/./urandom -Dweblogic.Name=%s -Dweblogic.management.server=http://%s:%s %s' % (msname, admin_host, admin_port, memargs)
arguments = arguments + ' ' + mswmargs

print('############################ Server JVM args: '+arguments+' ######################################')

cmo.setArguments(arguments)


cd('/')
cmo.createServer('MHC')

cd('/Servers/MHC')
cmo.setMachine(getMBean('/Machines/%s' % nmname))

cmo.setListenAddress(msinternal)
cmo.setListenPort(7059)
cmo.setListenPortEnabled(true)
cmo.setExternalDNSName(mshost)
cd('/Servers/MHC/SSL/MHC')
cmo.setEnabled(false)
cd('/Servers/MHC/ServerStart/MHC')
cmo.setArguments('-Dweblogic.MaxMessageSize=100000000 -Dmhc_simulator.properties.path=/app_config/mhc -Dweblogic.transaction.allowOverrideSetRollbackReason=true -Xrunjdwp:transport=dt_socket,address=8059,server=y,suspend=n')


cd('/JTA/base_domain')
cmo.setTimeoutSeconds(1800)

saveActivate()

# Exit
# =========
exit()
