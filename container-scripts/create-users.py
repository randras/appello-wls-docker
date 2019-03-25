import sys
#read properties file
 
if len(sys.argv) != 2:
	print "Invalid Arguments :: Please provide input file"
 	exit()
try:
	print "Load properties file"
	properties=sys.argv[1]
	file=open(properties,'r')
	print "Read properties file"
	exec file
	print "Execute properties file"
	file.close
except:
	exit()

print 'userName Array Values are : ',userNameArray
print 'Admin server user name : ',USER
print 'ADMIN Server URL : ',ADMIN_URL


connect(USER,PASSWORD,ADMIN_URL)
edit()
serverConfig()

successCount=0

cd('/SecurityConfiguration/ehc/Realms/myrealm/AuthenticationProviders/DefaultAuthenticator')

cmo.createGroup(userGroup, '')

for userName in userNameArray:
	usrName=userName['name']
	pwd=userName['userPwd']
	desc=userName['description']
	grpName1=userName['groupName1']	
	grpName2=userName['groupName2']	

	cmo.createUser(usrName,pwd,desc)
	print usrName,'- been created' 
	cmo.addMemberToGroup(grpName1,usrName)
	if grpName2 != null
		cmo.addMemberToGroup(grpName2,usrName)

	#cmo.addMemberToGroup(grpName3,usrName)
	print grpName1,'- been assigend to ',usrName
	successCount=successCount+1
	print str(successCount)+" users successfully created"