
import os

msname = os.environ.get('MS_NAME', 'KHC')

execfile('/u01/oracle/commonfuncs.py')

connectToAdmin()

# Start Managed Server
# ------------
try:
   start(msname, 'Server')
except:
   dumpStack()

# Exit
# =========
exit()
