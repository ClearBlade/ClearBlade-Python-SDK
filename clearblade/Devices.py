from __future__ import absolute_import
import json
from . import cbLogs
from . import restcall


def getDevices(system, authenticatedUser, query=None):
    if query:
        params = {}
        params["FILTERS"] = query.filters
        params["SORT"] = query.sorting
        params = {"query": json.dumps(params)}
    else:
        params = ""
    url = system.url + "/api/v/2/devices/" + system.systemKey
    resp = restcall.get(url, headers=authenticatedUser.headers, params=params, sslVerify=system.sslVerify)
    return resp


def getDevice(system, authenticatedUser, name):
    url = system.url + "/api/v/2/devices/" + system.systemKey + "/" + name
    resp = restcall.get(url, headers=authenticatedUser.headers, sslVerify=system.sslVerify)
    return resp


class Device:
    def __init__(self, system, name, key="", user=None):
        self.name = name
        self.systemKey = system.systemKey
        self.url = system.url + "/api/v/2/devices/" + self.systemKey
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.token = ""
        self.system = system
        if key != "":
            self.authorize(key)
        else:
            cbLogs.error("You must provide an active key when creating the device", name)
            exit(-1)

    def authorize(self, key):
        cbLogs.info("Authenticating", self.name, "as a device...")
        credentials = {
            "deviceName": self.name,
            "activeKey": key
        }
        resp = restcall.post(self.url + "/auth", headers=self.headers, data=credentials, sslVerify=self.system.sslVerify)
        self.token = str(resp["deviceToken"])
        self.headers["ClearBlade-DeviceToken"] = self.token
        cbLogs.info("Successfully authenticated!")

    def update(self, info):
        payload = info
        try:
            json.loads(payload)
        except TypeError:
            payload = json.dumps(payload)
        restcall.put(self.url + "/" + self.name, headers=self.headers, data=payload, sslVerify=self.system.sslVerify)
        cbLogs.info("Successfully updated", self.name)


###########################
#   DEVELOPER ENDPOINTS   #
###########################

def DEVnewDevice(developer, system, name, enabled=True, type="", state="", active_key="", allow_certificate_auth=False, allow_key_auth=True, certificate="", description="", keys=""):
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
    resp = restcall.post(url, headers=developer.headers, data=data, sslVerify=system.sslVerify)
    cbLogs.info("Successfully created", name, "as a device.")
    return resp


def DEVgetDevices(developer, system, query=None):
    if query:
        params = {}
        params["FILTERS"] = query.filters
        params["SORT"] = query.sorting
        params = {"query": json.dumps(params)}
    else:
        params = ""
    url = system.url + "/api/v/2/devices/" + system.systemKey
    resp = restcall.get(url, headers=developer.headers, params=params, sslVerify=system.sslVerify)
    return resp


def DEVgetDevice(developer, system, name):
    url = system.url + "/api/v/2/devices/" + system.systemKey + "/" + name
    resp = restcall.get(url, headers=developer.headers, sslVerify=system.sslVerify)
    return resp


def DEVupdateDevice(developer, system, name, updates):
    url = system.url + "/api/v/2/devices/" + system.systemKey + "/" + name
    resp = restcall.put(url, headers=developer.headers, data=updates, sslVerify=system.sslVerify)
    cbLogs.info("Successfully updated device:", name + ".")
    return resp


def DEVdeleteDevice(developer, system, name):
    url = system.url + "/api/v/2/devices/" + system.systemKey + "/" + name
    resp = restcall.delete(url, headers=developer.headers, sslVerify=system.sslVerify)
    cbLogs.info("Successfully deleted device:", name + ".")
    return resp
