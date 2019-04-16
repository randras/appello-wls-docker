
import os


domainname = os.environ.get('DOMAIN_NAME', 'base_domain')
domainhome = os.environ.get('DOMAIN_HOME', '/u01/oracle/user_projects/domains/' + domainname)

readDomain(domainhome)


jdbcResourcePath = '/JDBCSystemResources/'+dsname+'/JDBCResource/'+dsname+'/JDBCDataSourceParams/'+dsname

print 'JDBC resource path: ',jdbcResourcePath

cd(jdbcResourcePath)
cmo.setGlobalTransactionsProtocol('EmulateTwoPhaseCommit')

saveActivate()

updateDomain()
closeDomain()


exit()
