import cbLogs
import restcall
# import json


class Service():
    def __init__(self, system, name):
        self.name = name
        self.url = system.url + "/api/v/1/code/" + system.systemKey + "/" + name

    def execute(self, authenticatedUser, params={}):
        cbLogs.info("Executing code service", self.name)
        resp = restcall.post(self.url, headers=authenticatedUser.headers, data=params)
        return resp


class Library():
    def __init__(self):
        pass
