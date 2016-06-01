import restHelper
import urllib
import json

class ClearBlade:
	"""The class that creates all of the objects to interact with the ClearBlade Platform
	"""
	def __init__(self, systemKey, systemSecret, url='https://platform.clearblade.com'):
		self.systemKey = systemKey
		self.systemSecret = systemSecret
		self.headers = {
				'ClearBlade-AppKey': self.systemKey,
				'ClearBlade-AppSecret': self.systemSecret,
				'Content-Type': 'application/json'
				}
		self.url = url

	def NewCollection(self, collectionID):
		return Collection(self.systemKey, self.systemSecret, collectionID, url=self.url)

class Collection:
	"""The class that handles all collection-level operations
	"""
	def __init__(self, systemKey, systemSecret, collectionID, url='https://platform.clearblade.com'):
		self.systemKey = systemKey
		self.systemSecret = systemSecret
		self.collectionID = collectionID	
		self.headers = {
				'ClearBlade-AppKey': self.systemKey,
				'ClearBlade-AppSecret': self.systemSecret,
				'Content-Type': 'application/json'
				}
		self.url = url + '/api/' + self.collectionID
		self.rh = restHelper.restHelper(self.url, self.headers)

	def fetch(self, query=None):
		if query:
			return self.rh.get({'query':json.dumps(query)})
		else:
			return self.rh.get()

	def create(self, data):
		return self.rh.post(data)

	def update(self, changes, query):
		return self.rh.put({'query': query, '$set': changes})

	def delete(self, query):
		return self.rh.delete({'query': json.dumps(query)})

class Item:
	"""The class that handles all item-level operations and holds the data
	"""
	def __init__(self, systemKey, systemSecret, collectionID, itemID, data):
		self.systemKey = systemKey
		self.systemSecret = systemSecret
		self.collectionID = collectionID
		self.itemID = itemID
		self.data = data
