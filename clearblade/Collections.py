from __future__ import absolute_import
import json
from . import restcall
from . import cbLogs


class Collection():
    def __init__(self, system, authenticatedUser, collectionID="", collectionName=""):
        if collectionID:
            self.url = system.url + '/api/v/1/data/' + collectionID
            self.collectionID = collectionID
            self.collectionName = None
        elif collectionName:
            self.url = system.url + '/api/v/1/collection/' + system.systemKey + "/" + collectionName
            self.collectionName = collectionName
            self.collectionID = None
        else:
            cbLogs.error("You must supply either a collection name or id.")  # beep
            exit(-1)
        self.headers = authenticatedUser.headers
        self.currentPage = 0
        self.nextPageURL = None
        self.prevPageURL = None
        self.items = []
        self.sslVerify = system.sslVerify

    def getItems(self, query=None, pagesize=100, pagenum=1, url=""):
        url = self.url + url
        params = {
            "PAGESIZE": pagesize,
            "PAGENUM": pagenum
        }
        if query:
            params["FILTERS"] = query.filters
            params["SORT"] = query.sorting

        resp = restcall.get(url, headers=self.headers, params={"query": json.dumps(params)}, sslVerify=self.sslVerify)

        self.currentPage = resp["CURRENTPAGE"]
        self.nextPageURL = resp["NEXTPAGEURL"]
        if self.nextPageURL:
            self.nextPageURL = "?" + self.nextPageURL.split("/")[-1].split("?")[-1]
        self.prevPageURL = resp["PREVPAGEURL"]
        if self.prevPageURL:
            self.prevPageURL = "?" + self.prevPageURL.split("/")[-1].split("?")[-1]
        self.items = resp["DATA"]
        return self.items

    def getNextPage(self):
        if self.nextPageURL:
            return self.getItems(url=self.nextPageURL)
        else:
            cbLogs.info("No next page!")

    def getPrevPage(self):
        if self.prevPageURL:
            return self.getItems(url=self.prevPageURL)
        elif self.currentPage == 2:
            # apparently our api doesn't like to be consistent
            return self.getItems()
        else:
            cbLogs.info("No previous page!")

    def createItem(self, data):
        return restcall.post(self.url, headers=self.headers, data=data, sslVerify=self.sslVerify)

    def updateItems(self, query, data):
        payload = {
            "query": query.filters,
            "$set": data
        }
        return restcall.put(self.url, headers=self.headers, data=payload, sslVerify=self.sslVerify)

    def deleteItems(self, query):
        return restcall.delete(self.url, headers=self.headers, params={"query": json.dumps(query.filters)}, sslVerify=self.sslVerify)


###########################
#   DEVELOPER ENDPOINTS   #
###########################

def DEVgetAllCollections(developer, system):
    url = system.url + "/admin/allcollections"
    params = {
        "appid": system.systemKey
    }
    resp = restcall.get(url, headers=developer.headers, params=params, sslVerify=system.sslVerify)
    return resp

def DEVnewCollection(developer, system, name):
    url = system.url + "/admin/collectionmanagement"
    data = {
        "appID": system.systemKey,
        "name": name
    }
    resp = restcall.post(url, headers=developer.headers, data=data, sslVerify=system.sslVerify)
    cbLogs.info("Successfully created collection: " + name)
    return Collection(system, developer, collectionID=resp["collectionID"])

def DEVaddColumnToCollection(developer, system, collection, columnName, columnType):
    if not collection.collectionID:
        cbLogs.error("You must supply the collection id when adding a column to a collection.")
        exit(-1)
    url = system.url + "/admin/collectionmanagement"
    data = {
        "id": collection.collectionID,
        "addColumn": {
            "id": collection.collectionID,
            "name": columnName,
            "type": columnType
        }
    }
    resp = restcall.put(url, headers=developer.headers, data=data, sslVerify=system.sslVerify)
    cbLogs.info("Successfully added column: " + columnName)
    return resp

