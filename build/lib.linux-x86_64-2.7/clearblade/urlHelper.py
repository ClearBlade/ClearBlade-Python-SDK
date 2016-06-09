import urllib2
import urllib
import json

class Request(urllib2.Request):

	def __init__(self, 
			url, data=None, headers={},
			origin_req_host=None, unverifiable=False, method=None):
		self.url = url
		self.data = data
		self.origin_req_host = origin_req_host
		self.unverifiable = unverifiable
		self.method = method
		self.headers = headers
		urllib2.Request.__init__(self, self.url, self.data, self.headers, self.origin_req_host, self.unverifiable)
		self.opener = urllib2.build_opener(urllib2.HTTPHandler)

	def get_method(self):
		if self.method:
			return self.method

		return urllib2.Request.get_method()

	def open(self):
		return self.opener.open(self)
