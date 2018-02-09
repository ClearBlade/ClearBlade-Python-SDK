from __future__ import absolute_import
from . import cbLogs
from . import restcall


READ = 1
CREATE = 2
UPDATE = 4
DELETE = 8

###########################
#   DEVELOPER ENDPOINTS   #
###########################

def DEVsetPermissionsForCollection(developer, system, collection, permissionsLevel, roleName):
    url = system.url + "/admin/user/" + system.systemKey + "/roles"
    data = {
        "id": roleName,
        "changes": {
            "collections": [{
                "itemInfo": {
                    "name": collection.collectionName,
                    "id": collection.collectionID
                },
                "permissions": permissionsLevel
            }]
        }
    }
    resp = restcall.put(url, headers=developer.headers, data=data, sslVerify=system.sslVerify)
    cbLogs.info("Successfully updated permissions for role: " + roleName)
    return resp
    