import ldrpyutils.core
import pkg_resources

def test_single():
   filepath = pkg_resources.resource_filename("ldrpyutils", 'test/data/simple.xlsx')

   user = 'testuser'
   passwd = 'testpass'
   isMulti = False
   emitFile = False
   registry_url = 'http://example.org/register'
   updateOnlineRegisters = False
   verbose = True
   registry_auth_url = registry_url + "/system/security/apilogin"

   #expect fail
   resultFlag = ldrpyutils.core.load_simple_file(filepath, user, passwd, emitFile=emitFile,
                   registry_auth_url=registry_auth_url,
                   updateOnlineRegisters=updateOnlineRegisters,
                   verbose=verbose
                )
   assert resultFlag == False
