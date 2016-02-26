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
	# def __init__(self):
	# 	self.UserClient = {}
	# 	self.DevClient = {}

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
			resp = json.loads(resp.text)
			client.UserToken = str(resp['user_token'])	

		if isinstance(client, Client.DevClient) == True:
			resp = requests.post(self.CB_ADDR + "/admin/auth", data=json.dumps(payload))		
			print resp.text
			resp = json.loads(resp.text)
			client.DevToken = str(resp['dev_token'])					
			
	def authAnon(self, UserClient):
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

	def RegisterDevUser(self, username, password, UserClient):
		if UserClient.UserToken == "":
			print "Must be logged in to create user"
			exit(1)
		endpoint = "https://sandbox.clearblade.com/admin/user/" + UserClient.systemKey
		payload = {
			"email" : username,
			"password" : password
		}	
		resp = requests.post(endpoint, data=json.dumps(payload))
		print resp.text

# userClient = Client.UserClient("eeccc5eb0af8d5e6b5a4c094a474", "EECCC5EB0A90EBC6E09CEE95E65D", "test@clearblade.com", "rohanbendre")

# userClient = Client.UserClient("b6d590ec0a96a9f5b5f495a4b4d601", "B2DB90EC0A98FC88B186E0AAA5CE01", "test@clearblade.com", "Timtim_999")
# # # userClient.Auth()
# auth = Auth()
# auth.Authenticate(userClient)

# params = {"city" : "Austin"}
# code = Code.CodeService(userClient)
# code.CallService("ServicePart4", params, "false")

# auth.RegisterUser("registeruser@clearblade.com", "clearblade", userClient)
# # auth.RegisterUser("test1@clearblade.com", "clearblade", userClient)
# # auth.RegisterDevUser("test1@clearblade.com", "clearblade", userClient)
# # userAnon = UserClient.UserClient("8a83d9ec0a8aae92fba990ac9521", "8A83D9EC0AC2A38CAED8CFC6DFA101", "this email is empty", "")
# # auth.authAnon(userAnon)

# devClient = Client.DevClient("eeccc5eb0af8d5e6b5a4c094a474", "EECCC5EB0A90EBC6E09CEE95E65D", "rohan@clearblade.com", "rohanbendre")
# auth.Authenticate(devClient)


# message = Messaging.Messaging(devClient)
# message.printValue()
# message.InitializeMQTT()
# message.publishMessage("weather", "Testing", 0)
# message.subscribe("weather", 0)
# time.sleep(5)
# message.publishMessage("weather", "trying", 0)
# time.sleep(2)
# message.publishMessage("weather", "trying", 1)
# message.publishMessage("weather", "trying", 1)
# message.publishMessage("weather", "trying", 1)
# message.unsubscribe("weather")
# time.sleep(4)
# message.disconnect()
# time.sleep(4)
# auth.authAnon(userClient)

# auth.NewUserClient("8a83d9ec0a8aae92fba990ac9521", "8A83D9EC0AC2A38CAED8CFC6DFA101", "test@clearblade.com", "clearblade")
# auth.Authenticate(auth.DevClient)		