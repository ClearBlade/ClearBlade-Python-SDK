import urlHelper
import urllib
import json

def get(url, headers={}, data=None):
	if data:
		url = url + "?" + urllib.urlencode(data)
	req = urlHelper.Request(url, headers=headers, method='GET')
	return req.open()

def post(url, headers={}, data=None):
	if data:
		data = json.dumps(data)
	req = urlHelper.Request(url, data=data, headers=headers, method='POST')
	return req.open()

def put(url, headers={}, data=None):
	if data:
		data = json.dumps(data)
	req = urlHelper.Request(url, data=data, headers=headers, method='PUT')
	return req.open()

def delete(url, headers={}, data=None):
	if data:
		url = url + "?" + urllib.urlencode(data)
	req = urlHelper.Request(url, headers=headers, method='DELETE')
	return req.open()


class restHelper: 
	"""Used to have persistant headers between if you want to use just a request,
	try using one of the stand-alone methods
	"""
	def __init__(self, url, headers={}):
		self.url = url
		self.headers = headers

	def get(self, data=None):
		return get(self.url, headers=self.headers, data=data)

	def post(self, data=None):
		return post(self.url, headers=self.headers, data=data)

	def put(self, data=None):
		return put(self.url, headers=self.headers, data=data)

	def delete(self, data=None):
		return delete(self.url, headers=self.headers, data=data)
