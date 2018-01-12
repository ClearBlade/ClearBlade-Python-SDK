from __future__ import absolute_import
from . import restcall
from . import cbLogs


def registerUser(system, authenticatedUser, email, password):
    newUserCredentials = {
        "email": email,
        "password": password
    }
    cbLogs.info("Registering", email + "...")
    resp = restcall.post(authenticatedUser.url + "/reg", headers=authenticatedUser.headers, data=newUserCredentials, silent=True, sslVerify=system.sslVerify)
    try:
        newUser = User(system, email, password)
        newUser.token = str(resp["user_token"])
        newUser.headers["ClearBlade-UserToken"] = newUser.token
        cbLogs.info("Successfully registered", email + "as a user!")
        return newUser
    except TypeError:
        cbLogs.error(email, "already exists as a user on this system.")
        exit(-1)


class AnonUser(object):
    def __init__(self, system):
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "ClearBlade-SystemKey": system.systemKey,
            "ClearBlade-SystemSecret": system.systemSecret
        }
        self.system = system
        self.url = system.url + "/api/v/1/user"
        self.token = ""

    def authenticate(self):
        self.headers.pop("ClearBlade-UserToken", None)
        try:
            cbLogs.info("Authenticating", self.credentials["email"], "as a user...")
            resp = restcall.post(self.url + "/auth", headers=self.headers, data=self.credentials, sslVerify=self.system.sslVerify)
        except AttributeError:
            cbLogs.info("Authenticating as anonymous...")
            resp = restcall.post(self.url + "/anon", headers=self.headers, sslVerify=self.system.sslVerify)
        self.token = str(resp["user_token"])
        self.headers["ClearBlade-UserToken"] = self.token
        if self not in self.system.users:
            self.system.users.append(self)
        cbLogs.info("Successfully authenticated!")

    def logout(self):
        restcall.post(self.url + "/logout", headers=self.headers, sslVerify=self.system.sslVerify)
        if self in self.system.users:
            self.system.users.remove(self)
        try:
            cbLogs.info(self.credentials["email"], "has been logged out.")
        except AttributeError:
            cbLogs.info("Anonymous user has been logged out.")

    def checkAuth(self):
        resp = restcall.post(self.url + "/checkauth", headers=self.headers, silent=True, sslVerify=self.system.sslVerify)
        try:
            return resp["is_authenticated"]
        except TypeError:
            return False


class User(AnonUser):
    def __init__(self, system, email, password):
        super(User, self).__init__(system)
        self.credentials = {
            "email": email,
            "password": password
        }
