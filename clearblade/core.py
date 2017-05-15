import restHelper
import urllib
import json
import Client
import requests

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
	def __init__(self, client, collectionID):
		self.client = client
		self.collectionID = collectionID	
		self.headers = {
			'ClearBlade-SystemKey': self.client.systemKey,
			'ClearBlade-SystemSecret': self.client.systemSecret,
			'Content-Type': 'application/json'
		}
		if isinstance(self.client, Client.UserClient):
			self.headers['ClearBlade-UserToken'] = self.client.UserToken
		elif isinstance(self.client, Client.DevClient):
			self.headers['ClearBlade-DevToken'] = self.client.DevToken
		elif isinstance(self.client, Client.DeviceClient):
			self.headers['ClearBlade-DeviceToken'] = self.client.DeviceToken
		self.url = self.client.platform + '/api/v/1/data/' + self.collectionID

	def fetch(self, query=None):
		resp = None
		if query:
			resp = requests.get(self.url, headers=self.headers, params={'query': json.dumps(query)})
		else:
			resp = requests.get(self.url, headers=self.headers)
		if resp.status_code == 200:
			try:
				resp = json.loads(resp.text)
				return resp
			except ValueError:
				print("Failed to decode response JSON: {0}".format(resp.text))
		else:
			print("Request failed with status code: {0} and response text: {1}".format(resp.status_code, resp.text))

	def create(self, data):
		return self.rh.post(data)

	def update(self, changes, query):
		resp = requests.put(self.url,  headers=self.headers, json={'query': query, '$set': changes})
		print resp.request.body
		if resp.status_code == 200:
			try:
				resp = json.loads(resp.text)
				return resp
			except ValueError:
				print("Failed to decode response JSON: {0}".format(resp.text))
		else:
			print("Request failed with status code: {0} and response text: {1}".format(resp.status_code, resp.text))

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
