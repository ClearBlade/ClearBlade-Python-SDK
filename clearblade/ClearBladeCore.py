import atexit
import restcall
import Users
import Collections
import Messaging
import cbLogs

class System:
    def __exitcode(self):
        # forces all users to log out on system close.
        # I did this to prevent possible token reuse
        # after client code exits, even if they don't 
        # log their users out themselves.
        while self.users:
            self.users.pop(0).logout()

    def __init__(self,systemKey,systemSecret,url="https://platform.clearblade.com"):
        self.systemKey = systemKey
        self.systemSecret = systemSecret
        self.url = url
        self.users = []
        self.collections = []
        self.messagingClients = []
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

    def DevUser(self, email, password):
        dev = Users.DevUser(self, email, password)
        dev.authenticate()
        return dev

    def registerUser(self, authenticatedUser, email, password):
        Users.registerUser(self, authenticatedUser, email, password)

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
    
    def Messaging(self):  # TODO
        pass


class Query:
    def __init__(self, pagesize=100, pagenum=1):
        self.sorting = [] # only used in fetches. also, not implemented yet. TODO
        self.filters = []

    def Or(self, query): 
        # NOTE: you can't add filters after 
        # you Or two queries together
        q = Query()
        for filter in self.filters:
            q.filters.append(filter)
        for filter in query.filters:
            q.filters.append(filter)
        return q

    def __addFilter(self, column, value, operator):
        if len(self.filters)==0:
            self.filters.append([])
        self.filters[0].append({operator:[{column:value}]})

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







