import restcall
import cbLogs
import json


def registerDev(fname, lname, org, email, password, url="https://platform.clearblade.com"):
    newDevCredentials = {
        "fname": fname,
        "lname": lname,
        "org": org,
        "email": email,
        "password": password
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    cbLogs.info("Registering", email, "as a developer...")
    resp = restcall.post(url + '/admin/reg', headers=headers, data=newDevCredentials, silent=True)
    try:
        newDev = Developer(url, email, password)
        newDev.token = str(resp["dev_token"])
        newDev.headers["ClearBlade-DevToken"] = newDev.token
        cbLogs.info("Successfully registered", email, "as a developer!")
        return newDev
    except TypeError:
        cbLogs.error(email, "already exists as a developer at", url)
        exit(-1)


class Developer:
    def __init__(self, email, password, url="https://platform.clearblade.com"):
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
        self.authenticate()

    def authenticate(self):
        cbLogs.info("Authenticating", self.credentials["email"], "as a developer...")
        resp = restcall.post(self.url + "/admin/auth", headers=self.headers, data=self.credentials)
        self.token = str(resp["dev_token"])
        self.headers["ClearBlade-DevToken"] = self.token
        cbLogs.info("Successfully authenticated!")

    def logout(self):
        restcall.post(self.url + "/admin/logout", headers=self.headers)
        if self in self.system.users:
            self.system.users.remove(self)
        cbLogs.info(self.credentials["email"], "(developer) has been logged out.")

    ##########################
    # ~~~~~~~~~~~~~~~~~~~~~~ #
    #   DEV ONLY ENDPOINTS   #
    # ~~~~~~~~~~~~~~~~~~~~~~ #
    ##########################

    ###############
    #   Devices   #
    ###############

    def newDevice(self, system, name, enabled=True, type="", state="", active_key="", allow_certificate_auth=False, allow_key_auth=True, certificate="", description="", keys=""):
        url = system.url + "/admin/devices/" + system.systemKey + "/" + name
        data = {
            "active_key": active_key,
            "allow_certificate_auth": allow_certificate_auth,
            "allow_key_auth": allow_key_auth,
            "certificate": certificate,
            "description": description,
            "enabled": enabled,
            "keys": keys,
            "name": name,
            "state": state,
            "type": type
        }
        resp = restcall.post(url, headers=self.headers, data=data)
        cbLogs.info("Successfully created", name, "as a device.")
        return resp

    def getDevices(self, system, query=None):
        if query:
            params = {}
            params["FILTERS"] = query.filters
            params["SORT"] = query.sorting
            params = {"query": json.dumps(params)}
        else:
            params = ""
        url = system.url + "/api/v/2/devices/" + system.systemKey
        resp = restcall.get(url, headers=self.headers, params=params)
        return resp

    def getDevice(self, system, name):
        url = system.url + "/api/v/2/devices/" + system.systemKey + "/" + name
        resp = restcall.get(url, headers=self.headers)
        return resp

    def updateDevice(self, system, name, updates):
        url = system.url + "/api/v/2/devices/" + system.systemKey + "/" + name
        resp = restcall.put(url, headers=self.headers, data=updates)
        cbLogs.info("Successfully updated device:", name + ".")
        return resp

    def deleteDevice(self, system, name):
        url = system.url + "/api/v/2/devices/" + system.systemKey + "/" + name
        resp = restcall.delete(url, headers=self.headers)
        cbLogs.info("Successfully deleted device:", name + ".")
        return resp
