import paho.mqtt.client as mqtt
import thread
import time
import Client
import UserClient 
import math

class Messaging():
	CB_MSG_ADDR = "rtp.clearblade.com"
	def __init__(self, clientType):
		self.client = ""
		self.rc = 0
		self.clientType = clientType

	def printValue(self):
		if isinstance(self.clientType, Client.UserClient):
			print self.clientType.email
		if isinstance(self.clientType, Client.DevClient):
			print self.clientType.email	

	def InitializeMQTT(self):
		if isinstance(self.clientType, Client.UserClient):
			self.client = mqtt.Client(client_id=self.clientType.systemSecret, protocol=mqtt.MQTTv31)
			self.client.username_pw_set(self.clientType.UserToken, self.clientType.systemKey)
		if isinstance(self.clientType, Client.DevClient):
			self.client = mqtt.Client(client_id=self.clientType.systemSecret, protocol=mqtt.MQTTv31)
			self.client.username_pw_set(self.clientType.DevToken, self.clientType.systemSecret)
		
		def on_connect(client, flag, userdata, rc):
			if rc == 0:
				print "Connected successfully "
			else:
				print "Error in connection with code ", rc	
			self.rc = rc

		self.client.on_connect = on_connect
		
		self.client.connect(self.CB_MSG_ADDR, 1883, 60)
		self.client.loop_start()

	def publishMessage(self, topic, data, qos):	
		if isinstance(self.clientType, Client.UserClient) or isinstance(self.clientType, Client.DevClient):
			def on_publish(client, userdata, mid):
				print "Published", mid

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