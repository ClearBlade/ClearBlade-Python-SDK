from __future__ import absolute_import
from . import restcall
from . import cbLogs, cbErrors
from . import Collections
from . import Devices
from . import Permissions

def registerDev(fname, lname, org, email, password, url="https://platform.clearblade.com", registrationKey="", sslVerify=True):
    """Register Developer in environment"""
    newDevCredentials = {
        "fname": fname,
        "lname": lname,
        "org": org,
        "email": email,
        "password": password
    }
    if registrationKey != "":
        newDevCredentials["key"] = registrationKey
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    cbLogs.info("Registering", email, "as a developer...")
    resp = restcall.post(url + '/admin/reg', headers=headers, data=newDevCredentials, sslVerify=sslVerify)
    try:
        newDev = Developer(email, password, url, sslVerify=sslVerify, authOnCreate=False)
        newDev.token = str(resp["dev_token"])
        newDev.headers["ClearBlade-DevToken"] = newDev.token
        cbLogs.info("Successfully registered", email, "as a developer!")
        return newDev
    except TypeError:
        cbLogs.error(email, "already exists as a developer at", url)
        cbErrors.handle(-1)


class Developer:
    def __init__(self, email, password, url="https://platform.clearblade.com", sslVerify=True, authOnCreate=True):
        self.credentials = {
            "email": email,
            "password": password
        }
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.url = url
        self.token = ""
        self.sslVerify = sslVerify
        if not sslVerify:
            cbLogs.warn("You have disabled SSL verification, this should only be done if your ClearBlade Platform instance is leveraging self signed SSL certificates.")
        if authOnCreate:
            self.authenticate()

    def authenticate(self):
        """Authenticate Developer"""
        cbLogs.info("Authenticating", self.credentials["email"], "as a developer...")
        resp = restcall.post(self.url + "/admin/auth", headers=self.headers, data=self.credentials, sslVerify=self.sslVerify)
        self.token = str(resp["dev_token"])
        self.headers["ClearBlade-DevToken"] = self.token
        cbLogs.info("Successfully authenticated!")

    def logout(self):
        """Logout Developer"""
        restcall.post(self.url + "/admin/logout", headers=self.headers, sslVerify=self.sslVerify)
        if self in self.system.users:
            self.system.users.remove(self)
        cbLogs.info(self.credentials["email"], "(developer) has been logged out.")

    ##########################
    # ~~~~~~~~~~~~~~~~~~~~~~ #
    #   DEV ONLY ENDPOINTS   #
    # ~~~~~~~~~~~~~~~~~~~~~~ #
    ##########################

    #################
    #  Collections  #
    #################

    def getAllCollections(self, system):
        """Return all Collections as Developer"""
        return Collections.DEVgetAllCollections(self, system)

    def newCollection(self, system, name):
        """Create Collection as Developer"""
        return Collections.DEVnewCollection(self, system, name)

    def addColumnToCollection(self, system, collection, columnName, columnType):
        """Add Column to Collection as Developer"""
        return Collections.DEVaddColumnToCollection(self, system, collection, columnName, columnType)

    ###############
    #   Devices   #
    ###############

    def newDevice(self, system, name, enabled=True, type="", state="", active_key="", allow_certificate_auth=False, allow_key_auth=True, certificate="", description="", keys=""):
        """Create Device as Developer"""
        return Devices.DEVnewDevice(self, system, name, enabled, type, state, active_key, allow_certificate_auth, allow_key_auth, certificate, description, keys)

    def getDevices(self, system, query=None):
        """Return Devices as Developer"""
        return Devices.DEVgetDevices(self, system, query)

    def getDevice(self, system, name):
        """Return Device as Developer"""
        return Devices.DEVgetDevice(self, system, name)

    def updateDevice(self, system, name, updates):
        """Update Device as Developer"""
        return Devices.DEVupdateDevice(self, system, name, updates)

    def deleteDevice(self, system, name):
        """Delete Device as Developer"""
        return Devices.DEVdeleteDevice(self, system, name)

    #################
    #  Permissions  #
    #################

    def setPermissionsForCollection(self, system, collection, permissionsLevel, roleName):
        """Set Permissions for Collection as Developer"""
        return Permissions.DEVsetPermissionsForCollection(self, system, collection, permissionsLevel, roleName)

