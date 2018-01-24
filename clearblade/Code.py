from __future__ import absolute_import
from . import cbLogs
from . import restcall


class Service():
    def __init__(self, system, name):
        self.name = name
        self.url = system.url + "/api/v/1/code/" + system.systemKey + "/" + name
        self.sslVerify = system.sslVerify

    def execute(self, authenticatedUser, params={}):
        cbLogs.info("Executing code service", self.name)
        resp = restcall.post(self.url, headers=authenticatedUser.headers, data=params, sslVerify=self.sslVerify)
        return resp


class Library():
    def __init__(self):
        pass
