import paho.mqtt.client as mqtt
import thread
import time
import Client
import UserClient 
import math
import random
import string
from urlparse import urlparse

class Messaging():
	CB_MSG_ADDR = ""
	response = 0
	def __init__(self, clientType):
		self.client = ""
		self.rc = 0
		self.clientType = clientType
		self.CB_MSG_ADDR = urlparse(clientType.platform).netloc

	def printValue(self):
		if isinstance(self.clientType, Client.UserClient):
			print self.clientType.email
		if isinstance(self.clientType, Client.DevClient):
			print self.clientType.email	

	def InitializeMQTT(self, **keyword_parameters):
		if isinstance(self.clientType, Client.UserClient):
			self.client = mqtt.Client(client_id=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(23)), protocol=mqtt.MQTTv311)
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
			else:
				print "Here.. Error in connection with code ", rc

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