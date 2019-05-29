# Copyright (c) 2018 Oracle and/or its affiliates. All rights reserved.
#
# WLST Offline for deploying an application under APP_NAME packaged in APP_PKG_FILE located in APP_PKG_LOCATION
# It will read the domain under DOMAIN_HOME by default
#
# author: Bruno Borges <bruno.borges@oracle.com>
# since: December, 2015
#
import os


def getJMSModulePath(jms_module_name):
    jms_module_path = "/JMSSystemResource/"+jms_module_name+"/JmsResource/NO_NAME_0"
    print jms_module_path
    return jms_module_path

def getFSpath(jms_module_name,jms_fs_name):
    jms_module_path = getJMSModulePath(jms_module_name)
    jms_fs_path = jms_module_path+'/ForeignServer/'+jms_fs_name
    return jms_fs_path




def createFSJMSModule(jms_module_name,target_name):
    print 'createFSJMSModule start'
    cd('/')
    create(jms_module_name, "JMSSystemResource")
    assign('JMSSystemResource', jms_module_name, 'Target', target_name)
    print 'createFSJMSModule finished'

def createJMSFS(jms_module_name,cnurl,jms_fs_name):
    print 'createJMSFS start'
    jms_module_path = getJMSModulePath(jms_module_name)
    cd(jms_module_path)
    fs = create(jms_fs_name, 'ForeignServer')
    fs.setInitialContextFactory('weblogic.jndi.WLInitialContextFactory')
    fs.setConnectionURL(cnurl)
    fs.setDefaultTargetingEnabled(true)
    fs.unSet('JNDIPropertiesCredentialEncrypted')
    print 'createJMSFS finished'


def createFSdest(jms_module_name,jms_fs_name,jms_dest_name,ljndi,rjndi):
    print 'createFSdest start'
    cd('/')
    jms_fs_path = getFSpath(jms_module_name,jms_fs_name)
    cd(jms_fs_path)
    print jms_fs_path
    fd = create(jms_dest_name,'ForeignDestination')
    fd.setLocalJNDIName(ljndi)
    fd.setRemoteJNDIName(rjndi)
    print 'createFSdest finished'

def createFSconf(jms_module_name,jms_fs_name,jms_fconf_name,cljndi,crjndi):
    print 'createFSconf start'
    jms_fs_path = getFSpath(jms_module_name,jms_fs_name)
    cd(jms_fs_path)
    fcf = create(jms_fconf_name, 'ForeignConnectionFactory')
    fcf.setLocalJNDIName(cljndi)
    fcf.setRemoteJNDIName(crjndi)
    print 'createFSconf finished'


# Deployment Information
domainname = os.environ.get('DOMAIN_NAME', 'base_domain')
admin_name = os.environ.get('ADMIN_NAME', 'AdminServer')
domainhome = os.environ.get('DOMAIN_HOME', '/u01/oracle/user_projects/domains/' + domainname)
cms_fs_url = os.environ.get('CMS_FOREIGN_SERVER_URL')
val_fs_url = os.environ.get('VAL_FOREIGN_SERVER_URL')

msname = os.environ.get('MS_NAME', 'ManagedServer')

print('admin_name  : [%s]' % admin_name);

# Read Domain in Offline Mode
# ===========================
readDomain(domainhome)



# Create a JMS Server
# ===================
cd('/')
jmsserver=create('KH_CMS_JMS', 'JMSServer')
print('Create JMSServer : [%s]' % 'JMSServer')

cd('/')
assign('JMSServer', 'KH_CMS_JMS', 'Target', msname)

# Create a JMS System resource
# ============================
cd('/')
create('KH_CMS_JMSM', 'JMSSystemResource')
cd('JMSSystemResource/KH_CMS_JMSM/JmsResource/NO_NAME_0')

# Create a JMS Queue and its subdeployment
# ========================================
myq = create('KHInQueue','Queue')
myq.setJNDIName('jms/KHInQueue')
myq.setSubDeploymentName('KH_CMS_SD')

myq = create('KHInSyncQueue','Queue')
myq.setJNDIName('jms/KHInSyncQueue')
myq.setSubDeploymentName('KH_CMS_SD')

myq = create('KHInXLQueue','Queue')
myq.setJNDIName('jms/KHInXLQueue')
myq.setSubDeploymentName('KH_CMS_SD')

myq = create('KHOutQueue','Queue')
myq.setJNDIName('jms/KHOutQueue')
myq.setSubDeploymentName('KH_CMS_SD')

myq = create('KHOutXLQueue','Queue')
myq.setJNDIName('jms/KHOutXLQueue')
myq.setSubDeploymentName('KH_CMS_SD')


myq = create('KHConnectionFactory','ConnectionFactory')
myq.setJNDIName('jms/KHConnectionFactory')
myq.setSubDeploymentName('KH_CMS_SD')

cd('/JMSSystemResource/KH_CMS_JMSM')
create('KH_CMS_SD', 'SubDeployment')

# Target resources to the servers
# ===============================
cd('/')
assign('JMSSystemResource.SubDeployment', 'KH_CMS_JMSM.KH_CMS_SD', 'Target', 'KH_CMS_JMS')
assign('JMSSystemResource', 'KH_CMS_JMSM', 'Target', msname)


# Create a MHC System resource
# ============================

createFSJMSModule('MHC_JMSM', 'MHC')

createJMSFS('MHC_JMSM', cms_fs_url,'KH_CMS_Dev_FS')
createJMSFS('MHC_JMSM', val_fs_url,'KH_VAL_Dev_FS')

createFSdest('MHC_JMSM','KH_CMS_Dev_FS','KHCMSDevInQueue','jms/KHCMSDevInQueue','jms/KHInQueue')
createFSdest('MHC_JMSM','KH_CMS_Dev_FS','KHCMSDevInXLQueue','jms/KHCMSDevInXLQueue','jms/KHInXLQueue')
createFSdest('MHC_JMSM','KH_CMS_Dev_FS','KHCMSDevOutQueue','jms/KHCMSDevOutQueue','jms/KHOutQueue')
createFSdest('MHC_JMSM','KH_CMS_Dev_FS','KHCMSDevOutXLQueue','jms/KHCMSDevOutXLQueue','jms/KHOutXLQueue')

createFSdest('MHC_JMSM','KH_VAL_Dev_FS','KHVALDevInQueue','jms/KHVALDevInQueue','jms/KHVALInQueue')
createFSdest('MHC_JMSM','KH_VAL_Dev_FS','KHVALDevInXLQueue','jms/KHVALDevInXLQueue','jms/KHVALInXLQueue')
createFSdest('MHC_JMSM','KH_VAL_Dev_FS','KHVALDevOutQueue','jms/KHVALDevOutQueue','jms/KHVALOutQueue')
createFSdest('MHC_JMSM','KH_VAL_Dev_FS','KHVALDevOutXLQueue','jms/KHVALDevOutXLQueue','jms/KHVALOutXLQueue')

createFSconf('MHC_JMSM','KH_VAL_Dev_FS','KHVALDevQueueCF','jms/KHVALDevQueueCF', 'jms/KHVALConnectionFactory')
createFSconf('MHC_JMSM','KH_CMS_Dev_FS','KHCMSDevQueueCF','jms/KHCMSDevQueueCF', '	jms/KHConnectionFactory')

# Update Domain, Close It, Exit
# ==========================
updateDomain()
closeDomain()
exit()
