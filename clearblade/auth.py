import restHelper
import urllib
import json 
import urlHelper
import requests
import UserClient
import DevClient
import Code

import Client
import Messaging
import time 

class Auth(): 

	CB_ADDR = "https://rtp.clearblade.com"

	def Authenticate(self, client):
		payload = {
			"email" : client.email,
			"password" : client.password
		}

		if isinstance(client, Client.UserClient) == True:
			headers = {
				"Content-Type" : "application/json",
				"Accept" : "application/json",
				"ClearBlade-SystemSecret" : client.systemSecret,
				"ClearBlade-SystemKey" : client.systemKey
			}
			resp = requests.post(self.CB_ADDR + "/api/v/1/user/auth", data=json.dumps(payload), headers=headers)		
			print resp.text
			try:
				resp = json.loads(resp.text)
				client.UserToken = str(resp['user_token'])	
			except ValueError:
				print "JSON Decode has failed because of error : ", resp.text	

		if isinstance(client, Client.DevClient) == True:
			resp = requests.post(self.CB_ADDR + "/admin/auth", data=json.dumps(payload))		
			print resp.text
			try:
				resp = json.loads(resp.text)
				client.DevToken = str(resp['dev_token'])					
			except ValueError:
				print "JSON Decode has failed because of error : ", resp.text	
			
	def authAnon(self, client):
		headers = {
			"Content-Type" : "application/json",
			"Accept" : "application/json",
			"ClearBlade-SystemSecret" : UserClient.systemSecret,
			"ClearBlade-SystemKey" : UserClient.systemKey
		}
		resp = requests.post(self.CB_ADDR + "/api/v/1/user/anon", headers=headers)
		print resp.text

	def RegisterUser(self, username, password, client):
		if client.UserToken == "":
			print "Must be logged in to create user"
			exit(1)
		endpoint = self.CB_ADDR + "/api/v/1/user/reg"
		payload = {
			"email" : username,
			"password" : password
		}
		headers = {
			"ClearBlade-SystemSecret" : client.systemSecret,
			"ClearBlade-SystemKey" : client.systemKey,
			"ClearBlade-UserToken" : client.UserToken
		}	
		resp = requests.post(endpoint, data=json.dumps(payload), headers=headers)
		print resp.text
		try:
			resp = json.loads(resp.text)
			client.UserToken = str(resp['user_id'])
		except ValueError:
				print "JSON Decode has failed because of error : ", resp.text			

	def RegisterDevUser(self, username, password, client):
		if client.DevToken == "":
			print "Must be logged in to create user"
			exit(1)
		endpoint = self.CB_ADDR + "/admin/user/" + client.systemKey
		payload = {
			"email" : username,
			"password" : password
		}	
		headers = {
			"ClearBlade-SystemSecret" : client.systemSecret,
			"ClearBlade-SystemKey" : client.systemKey,
			"ClearBlade-DevToken" : client.DevToken
		}	
		resp = requests.post(endpoint, data=json.dumps(payload), headers=headers)
		print resp.text
		try:
			resp = json.loads(resp.text)	
			client.DevToken = str(resp['user_id'])	
		except ValueError:
				print "JSON Decode has failed because of error : ", resp.text	