import cbLogs
import restcall
import json


def getDevices(authenticatedUser, query=None):
    if query:
        params = {}
        params["FILTERS"] = query.filters
        params["SORT"] = query.sorting
        params = {"query": json.dumps(params)}
    else:
        params = ""
    url = authenticatedUser.system.url + "/api/v/2/devices/" + authenticatedUser.system.systemKey
    resp = restcall.get(url, headers=authenticatedUser.headers, params=params)
    return resp


class Device:
    def __init__(self, system, name):
        self.name = name
        self.systemKey = system.systemKey
        self.url = system.url + "/api/v/2/devices/" + self.systemKey
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.token = ""

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

    def update(self, info):  # TODO
        pass
