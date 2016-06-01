import paho.mqtt.client as mqtt
import thread
import time
import Client
import UserClient 
import math
import random
import string
import auth
from urlparse import urlparse

class Messaging():
	CB_MSG_ADDR = ""
	response = 0
	keep_alive = 30
	subscribeDict = dict()
	def __init__(self, clientType):
		self.client = ""
		self.rc = 0
		self.clientType = clientType
		self.CB_MSG_ADDR = urlparse(clientType.platform).netloc
		self.auth = auth.Auth()

	def printValue(self):
		if isinstance(self.clientType, Client.UserClient):
			print self.clientType.email
		if isinstance(self.clientType, Client.DevClient):
			print self.clientType.email	

	def InitializeMQTT(self, **keyword_parameters):
		print("Inside initialize")
		if isinstance(self.clientType, Client.UserClient):
			self.client = mqtt.Client(client_id=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(23)), clean_session=True, userdata=None, protocol=mqtt.MQTTv311)
			self.client.username_pw_set(self.clientType.UserToken, self.clientType.systemKey)
			print self.clientType.UserToken
		if isinstance(self.clientType, Client.DevClient):
			self.client = mqtt.Client(client_id=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(23)), protocol=mqtt.MQTTv311)
			self.client.username_pw_set(self.clientType.DevToken, self.clientType.systemKey)
		
		def on_connect(client, flag, userdata, rc):
			self.response = 1
			self.rc = rc
			if self.rc == 0:
				print flag
				print userdata
				print client
				print "Connected successfully "

				for topic, qos in self.subscribeDict.iteritems():
					self.subscribeNew(topic,qos)
					print "SUBSCRIBING "+topic+", "+str(qos)
			else:
				print "Error in connection with code ", str(rc)+"... Trying to reconnect"
				self.reconnectFunction()
			

		def on_log(client, userdata, level, buf):
			print "Inside log : ", buf	

		self.client.on_connect = on_connect
		self.on_log = on_log

		if ('keep_alive' in keyword_parameters):
			print "Timeout is : ", keyword_parameters['keep_alive']
			self.client.connect(self.CB_MSG_ADDR, 1883, keyword_parameters['keep_alive'])
			self.client.loop_start()
		else:	
			print "Attempting to connect now"
			self.client.connect_async(self.CB_MSG_ADDR, 1883, keepalive=30)
			self.client.loop_start()

		while(self.response !=1):
			continue

		if self.rc > 0:
			self.client.loop_stop()
			return self.rc		
		
	def publishMessage(self, topic, data, qos):	
		if isinstance(self.clientType, Client.UserClient) or isinstance(self.clientType, Client.DevClient):
			def on_publish(client, userdata, mid):
				print "Published", client

			self.client.on_publish = on_publish	
			self.client.publish(topic, data, qos)

	def subscribe(self, topic, qos):
		if isinstance(self.clientType, Client.UserClient) or isinstance(self.clientType, Client.DevClient):
			if topic in self.subscribeDict:
				print "Already subscribed to the topic"
			else:
				self.subscribeDict[topic] = qos
			thread.start_new_thread(self.keepSubscribed, (topic,qos))

	def subscribeNew(self, topic, qos):
		if isinstance(self.clientType, Client.UserClient) or isinstance(self.clientType, Client.DevClient):
			thread.start_new_thread(self.keepSubscribed, (topic,qos))		
		
	def keepSubscribed(self,topic,qos):

		def on_subscribe(client, userdata, mid, gqos):
			print "Subscribed"

		def on_message(client, obj,msg):
			print msg.payload

		self.client.subscribe(topic, qos)
		self.client.on_subscribe = on_subscribe
		self.client.on_message = on_message

	def unsubscribe(self, topic):
		if isinstance(self.clientType, Client.UserClient) or isinstance(self.clientType, Client.DevClient):
			print("Inside unsubscribed")
			self.client.unsubscribe(topic)
			self.subscribeDict.pop(topic, None)
			def on_unsubscribe(client, userdata, mid):
				print "Unsubscribed ",mid
			self.client.on_unsubscribe = on_unsubscribe

	def disconnect(self):
		if isinstance(self.clientType, Client.UserClient) or isinstance(self.clientType, Client.DevClient):
			def on_disconnect(client, userdata, rc):
				print "Disconnected"	
			self.client.disconnect()
			self.client.on_disconnect = on_disconnect
			self.client.loop_stop()

	def reconnectFunction(self):
		print("Inside reconnect function")
		#userClient = Client.UserClient("cecdeef40a98c1e1cb87c58dad58", "CECDEEF40A869A818AC6D9D4C21F", "parent@acme.com", "edge", "http://localhost") 
		userClient = self.clientType
		self.auth.Authenticate(userClient)
		self.clientType = userClient
		if isinstance(self.clientType, Client.UserClient):
			#self.client = mqtt.Client(client_id=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(23)), clean_session=True, userdata=None, protocol=mqtt.MQTTv311)
			#self.client.reinitialise(client_id=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(23)), clean_session=True, userdata=None)
			self.client.disconnect()
			self.client.username_pw_set(self.clientType.UserToken, self.clientType.systemKey)
			#print "###"+self.clientType.UserToken+"###"
			#print self.clientType.systemKey
			#self.client.connect(self.CB_MSG_ADDR, 1883, self.keep_alive)
			self.client.reconnect()
			self.client.loop_start()
			print "reinitialise"
		if isinstance(self.clientType, Client.DevClient):
			self.client = mqtt.Client(client_id=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(23)), protocol=mqtt.MQTTv311)
			self.client.username_pw_set(self.clientType.DevToken, self.clientType.systemKey)
