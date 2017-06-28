import restcall
import json
import cbLogs


class Collection():
    def __init__(self, system, authenticatedUser, collectionID="", collectionName=""):
        if collectionID:
            self.url = system.url + '/api/v/1/data/' + collectionID
        elif collectionName:
            self.url = system.url + '/api/v/1/collection/' + system.systemKey + "/" + collectionName
        else:
            cbLogs.error("beep")
            exit(-1)
        self.headers = authenticatedUser.headers
        self.currentPage = 0
        self.nextPageURL = None
        self.prevPageURL = None
        self.items = []

    def getItems(self, query=None, url="", pagesize=100, pagenum=1):
        url = self.url + url
        params = {
            "PAGESIZE": pagesize,
            "PAGENUM": pagenum
        }
        if query:
            params["FILTERS"] = query.filters
            params["SORT"] = query.sorting

        resp = restcall.get(url, headers=self.headers, params={"query": json.dumps(params)})

        self.currentPage = resp["CURRENTPAGE"]
        self.nextPageURL = resp["NEXTPAGEURL"]
        if self.nextPageURL:
            self.nextPageURL = "?" + self.nextPageURL.split("/")[-1].split("?")[-1]
        self.prevPageURL = resp["PREVPAGEURL"]
        if self.prevPageURL:
            self.prevPageURL = "?" + self.prevPageURL.split("/")[-1].split("?")[-1]
        self.items = resp["DATA"]
        return self.items

    def getNextPage(self, query=None):
        if self.nextPageURL:
            self.getItems(query, url=self.nextPageURL)
        else:
            cbLogs.info("No next page!")

    def getPrevPage(self, query=None):
        if self.prevPageURL:
            self.getItems(query, url=self.prevPageURL)
        elif self.currentPage == 2:
            # apparently our api doesn't like to be consistent
            self.getItems(query)
        else:
            cbLogs.info("No previous page!")

    def createItem(self, data):
        return restcall.post(self.url, headers=self.headers, data=data)

    def updateItems(self, query, data):
        payload = {
            "query": query.filters,
            "$set": data
        }
        return restcall.put(self.url, headers=self.headers, data=payload)

    def deleteItems(self, query):
        return restcall.delete(self.url, headers=self.headers, params={"query": json.dumps(query.filters)})
