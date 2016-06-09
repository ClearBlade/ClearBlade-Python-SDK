import Client
import requests
import json

class CodeService():
	CB_ADDR = "https://rtp.clearblade.com"
	CODE_PREAMBLE = "/api/v/1/code/"
	def __init__(self, clientType):
		self.clientType = clientType

	def CallService(self, name, params, log):
		creds = {
			"ClearBlade-SystemSecret" : self.clientType.systemSecret,
			"ClearBlade-SystemKey" : self.clientType.systemKey,
			"ClearBlade-UserToken" : self.clientType.UserToken 
		}
		if isinstance(self.clientType, Client.UserClient):
			resp = requests.post(self.CB_ADDR + self.CODE_PREAMBLE + self.clientType.systemKey + "/" + name, data=json.dumps(params), headers=creds)
			print resp.text