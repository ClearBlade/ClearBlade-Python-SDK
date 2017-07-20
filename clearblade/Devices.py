import cbLogs
import restcall
import json


def getDevices(system, authenticatedUser, query=None):
    if query:
        params = {}
        params["FILTERS"] = query.filters
        params["SORT"] = query.sorting
        params = {"query": json.dumps(params)}
    else:
        params = ""
    url = system.url + "/api/v/2/devices/" + system.systemKey
    resp = restcall.get(url, headers=authenticatedUser.headers, params=params)
    return resp


def getDevice(system, authenticatedUser, name):
    url = system.url + "/api/v/2/devices/" + system.systemKey + "/" + name
    resp = restcall.get(url, headers=authenticatedUser.headers)
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
            self.authorize(key)  # use an active key to auth
        elif user:
            self.autoAuthorize(name, user)  # use an authenticated user to pull the active key and auth with it
        else:
            cbLogs.error("You must provide an active key when creating the device", name)
            exit(-1)

    def authorize(self, key):
        cbLogs.info("Authenticating", self.name, "as a device...")
        credentials = {
            "deviceName": self.name,
            "activeKey": key
        }
        resp = restcall.post(self.url + "/auth", headers=self.headers, data=credentials)
        self.token = str(resp["deviceToken"])
        self.headers["ClearBlade-DeviceToken"] = self.token
        cbLogs.info("Successfully authenticated!")

    def autoAuthorize(self, name, user):
        resp = restcall.get(self.url + "/" + name, headers=user.headers)
        self.authorize(resp["active_key"])

    def update(self, info):
        payload = info
        try:
            json.loads(payload)
        except TypeError:
            payload = json.dumps(payload)
        restcall.put(self.url + "/" + self.name, headers=self.headers, data=payload)
        cbLogs.info("Successfully updated", self.name)
