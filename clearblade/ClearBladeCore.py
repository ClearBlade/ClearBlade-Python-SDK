from __future__ import absolute_import
import atexit
from . import Users
from . import Devices
from . import Collections
from . import Messaging
from . import Code
from .Developers import *  # allows you to import Developer from ClearBladeCore
from . import cbLogs


class System:
    def __exitcode(self):
        # forces all users to log out on system close.
        # I did this to prevent possible token reuse
        # after client code exits, even if they don't
        # log their users out themselves.
        while self.users:
            self.users.pop(0).logout()

    def __init__(self, systemKey, systemSecret, url="https://platform.clearblade.com", safe=True, sslVerify=True):
        self.systemKey = systemKey
        self.systemSecret = systemSecret
        self.url = url
        self.users = []
        self.collections = []
        self.messagingClients = []
        self.devices = []
        self.sslVerify = sslVerify
        if not sslVerify:
            cbLogs.warn("You have disabled SSL verification, this should only be done if your ClearBlade Platform instance is leveraging self signed SSL certificates.")
        if safe:
            atexit.register(self.__exitcode)

    #############
    #   USERS   #
    #############

    def User(self, email, password):
        user = Users.User(self, email, password)
        user.authenticate()
        return user

    def AnonUser(self):
        anon = Users.AnonUser(self)
        anon.authenticate()
        return anon

    def registerUser(self, authenticatedUser, email, password):
        n00b = Users.registerUser(self, authenticatedUser, email, password)
        self.users.append(n00b)
        return n00b

    ###############
    #   DEVICES   #
    ###############

    def getDevices(self, authenticatedUser, query=None):
        self.devices = Devices.getDevices(self, authenticatedUser, query)
        return self.devices

    def getDevice(self, authenticatedUser, name):
        dev = Devices.getDevice(self, authenticatedUser, name)
        return dev

    def Device(self, name, key):
        dev = Devices.Device(system=self, name=name, key=key)
        # check if dev in self.devices?
        return dev

    ############
    #   DATA   #
    ############

    def Collection(self, authenticatedUser, collectionID="", collectionName=""):
        if not collectionID and not collectionName:
            cbLogs.error("beep")
            exit(-1)
        col = Collections.Collection(self, authenticatedUser, collectionID, collectionName)
        self.collections.append(col)
        return col

    ############
    #   MQTT   #
    ############

    def Messaging(self, user, port=1883, keepalive=30, url=""):
        msg = Messaging.Messaging(user, port, keepalive, url)
        self.messagingClients.append(msg)
        return msg

    ############
    #   CODE   #
    ############

    def Service(self, name):
        return Code.Service(self, name)


class Query:
    def __init__(self):
        self.sorting = []  # only used in fetches. also, not implemented yet. TODO
        self.filters = []

    def Or(self, query):
        # NOTE: you can't add filters after
        # you Or two queries together.
        # This function has to be the last step.
        q = Query()
        for filter in self.filters:
            q.filters.append(filter)
        for filter in query.filters:
            q.filters.append(filter)
        return q

    def __addFilter(self, column, value, operator):
        if len(self.filters) == 0:
            self.filters.append([])
        self.filters[0].append({operator: [{column: value}]})

    def equalTo(self, column, value):
        self.__addFilter(column, value, "EQ")

    def greaterThan(self, column, value):
        self.__addFilter(column, value, "GT")

    def lessThan(self, column, value):
        self.__addFilter(column, value, "LT")

    def greaterThanEqualTo(self, column, value):
        self.__addFilter(column, value, "GTE")

    def lessThanEqualTo(self, column, value):
        self.__addFilter(column, value, "LTE")

    def notEqualTo(self, column, value):
        self.__addFilter(column, value, "NEQ")

    def matches(self, column, value):
        self.__addFilter(column, value, "RE")
