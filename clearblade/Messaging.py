import paho.mqtt.client as mqtt
import time
import sys
import Client
import math
import random
import string
import auth
from urlparse import urlparse

class Messaging():
	CB_MSG_ADDR = ""
	keep_alive = 30
	subscribeDict = dict()
        onMessageCallback = None
        onUnsubscribeCallback = None
        onDisconnectCallback = None
        onPublishCallback = None
        onSubscribeCallback = None
        
	def __init__(self, clientType):
		self.client = ""
		self.clientType = clientType
		self.CB_MSG_ADDR = urlparse(clientType.platform).netloc.split(':')
		self.CB_MSG_ADDR = self.CB_MSG_ADDR[0]
		self.auth = auth.Auth()

	def printValue(self):
		if isinstance(self.clientType, Client.UserClient):
			print "User : "+self.clientType.email
		if isinstance(self.clientType, Client.DevClient):
			print "Developer : "+self.clientType.email	

	def InitializeMQTT(self, **keyword_parameters):
		if isinstance(self.clientType, Client.UserClient):
			self.client = mqtt.Client(client_id=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(23)), clean_session=True, userdata=None, protocol=mqtt.MQTTv311)
			self.client.username_pw_set(self.clientType.UserToken, self.clientType.systemKey)
		if isinstance(self.clientType, Client.DevClient):
			self.client = mqtt.Client(client_id=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(23)), protocol=mqtt.MQTTv311)
			self.client.username_pw_set(self.clientType.DevToken, self.clientType.systemKey)
                if isinstance(self.clientType, Client.DeviceClient):
                        self.client = mqtt.Client(client_id=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(23)), protocol=mqtt.MQTTv311)
                        self.client.username_pw_set(self.clientType.DeviceToken, self.clientType.systemKey)
                if ('keep_alive' in keyword_parameters):
                        self.keep_alive = keyword_parameters['keep_alive']
                else:
                        #default
                        self.keep_alive = 30

                def resetOnRedial(client,userdata,rc):
                        if rc == 0:
                                #we actually did it!
                                #now we should reset any callbacks and various subscriptions
                                if self.onMessageCallback is not None:
                                        self.client.on_message = self.onMessageCallback
                                if self.onUnsubscribeCallback is not None:
                                        self.client.on_unsubscribe = self.onUnsubscribeCallback        
                                if self.onDisconnectCallback is not None:
                                        self.client.on_disconnect = self.onDisconnectCallback
                                if self.onPublishCallback is not None:
                                        self.client.on_publish = self.onPublishCallback
                                if self.onSubscribeCallback is not None:
                                        self.client.on_subscribe = self.onSubscribeCallback
                                for topic,qos in self.subscribeDict.iteritems():
                                        self.client.subscribe(topic,qos)
                        else:
                                self.resetClient()

                #we're supposed to attempt to reauth if connect fails
                self.client.on_connect = resetOnRedial
                self.client.connect_async(self.CB_MSG_ADDR, 1883, keepalive=self.keep_alive)
                self.client.loop_start()
		
	def publishMessage(self, topic, data, qos, cb=None):	
		if isinstance(self.clientType, Client.UserClient) or isinstance(self.clientType, Client.DevClient) or isinstance(self.clientType, Client.DeviceClient):
                        if cb is not None:
                                self.setOnPublishCallback(cb)

                        try:
                                self.client.publish(topic, data, qos)
                        except:
                                print sys.exc_info

	def subscribe(self, topic, qos, onMessageCallback=None):
		if isinstance(self.clientType, Client.UserClient) or isinstance(self.clientType, Client.DevClient) or isinstance(self.clientType, Client.DeviceClient):
                        if onMessageCallback is not None:
                                self.setOnMessageCallback(onMessageCallback)
                                
			if topic in self.subscribeDict:
                                #not sure if raising an exception is the proper thing here
                                #this method didn't return anything previously
                                raise Exception("Already subscribed on topic")
			else:
				self.subscribeDict[topic] = qos
                                self.client.subscribe(topic,qos)


        def setOnMessageCallback(self, onMessageCallback):
                """Sets the "on_message" callback. The method is called every time a message is received, no matter the topic. For more information see the paho mqtt documentation"""
                self.onMessageCallback = onMessageCallback
                self.client.on_message = self.onMessageCallback
        def setOnPublishCallback(self,cb):
                self.onPublishCallback = cb
                self.client.on_publish = self.onPublishCallback
        def setOnSubscribeCallback(self, onSubscribeCallback):
                self.onSubscribeCallback = onSubscribeCallback
                self.client.on_subscribe = self.onSubscribeCallback
        def setOnUnsubscribeCallback(self, onUnsubscribeCallback):
                """Sets the "on_unsubscribe" callback. Called when unsubscribe is called"""
                self.onUnsubscribeCallback = onUnsubscribeCallback
                self.client.on_onunsubscribe = onUnsubscribeCallback

        def setOnDisconnectCallback(self, onDisconnectCallback):
                """Sets the "on_disconnect" callback. By default it is set to reauthenticate, redial, and resubscribe, unless "disconnect" is specifically called"""
                self.onDisconnectCallback = onDisconnectCallback
                self.client.on_disconnect = onDisconnectCallback

        def setOnConnectCallback(self, onConnectCallback):
                self.onConnectCallback = onConnectCallback
                self.client.on_connect = onConnectCallback
                
        def subscribeNew(self, topic, qos):
		if isinstance(self.clientType, Client.UserClient) or isinstance(self.clientType, Client.DevClient) or isinstance(self.clientType, Client.DeviceClient):
                        self.subscribe(topic,qos)

        #preserving for backwards compat
        #a normal subscribe
        def keepSubscribed(self,topic,qos):
                self.subscribe(topic,qos)
        
	def unsubscribe(self, topic, onUnsubscribeCallback=None):
		if isinstance(self.clientType, Client.UserClient) or isinstance(self.clientType, Client.DevClient) or isinstance(self.clientType, Client.DeviceClient):
                        if onUnsubscribeCallback is not None:
                                self.setOnSubscribeCallback(onUnsubscribeCallback)
                        #should we check for unsubscribe in the dict?
                        self.client.unsubscribe(topic)
			self.subscribeDict.pop(topic, None)

	def disconnect(self,onDisconnectCallback=None):
		if isinstance(self.clientType, Client.UserClient) or isinstance(self.clientType, Client.DevClient) or isinstance(self.clientType, Client.DeviceClient):
                        if onDisconnectCallback is not None:
                                self.setOnDisconnectCallback(onDisconnectCallback)
			self.client.disconnect()
			self.client.loop_stop()


        def resetClient(self):
                #not sure if required?
                #previous behavior is to reauthenticate and try again if the connect fails
                self.auth.Authenticate(self.clientType)
                if isinstance(self.clientType, Client.UserClient):
                        self.client.username_pw_set(self.clientType.UserToken, self.clientType.systemKey)
                elif isinstance(self.clientType,Client.DevClient):
                        self.client.username_pw_set(self.clientType.DevToken, self.clientType.systemKey)
                elif isinstance(self.clientType, Client.DeviceClient):
                        self.client.username_pw_set(self.clientType.DeviceToken, self.clientType.systemKey)
                self.client.connect_async(self.CB_MSG_ADDR, 1883, keepalive=self.keep_alive)
