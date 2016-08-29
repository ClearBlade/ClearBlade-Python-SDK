import paho.mqtt.client as mqtt
import threading
import time
import Client
import UserClient 
import string
import auth
import Messaging
import zmq

class zmq2mqtt():

	def __init__(self, userClient, bindAddress):
		self.userClient = userClient
		self.bindAddress = bindAddress
		self.auth = auth.Auth()
		self.auth.Authenticate(self.userClient)
		self.message = Messaging.Messaging(self.userClient)
		self.status = self.message.InitializeMQTT()
		self.zmqSub(self.message, self.bindAddress)
		

	def zmqSub(self, message, bindAddress):
		pass
		# ZeroMQ Context
		context = zmq.Context()

		# Define the socket using the "Context"
		sock = context.socket(zmq.SUB)

		# Define subscription and messages with prefix to accept.
		sock.setsockopt(zmq.SUBSCRIBE, "1")
		sock.connect(str(self.bindAddress))

		while True:
		    recMessage= sock.recv()
		    print "Your message is "+recMessage
		    self.mqttPub(recMessage)

    	def mqttPub(self, message):
    		self.message.publishMessage("zmq/publish", str(message), 1)



if __name__ == '__main__':
	userClient = Client.UserClient("cecdeef40a98c1e1cb87c58dad58", "CECDEEF40A869A818AC6D9D4C21F", "parent@acme.com", "edge", "http://localhost") 
	bindAddress = "tcp://127.0.0.1:7777"
	zmq2mqtt = zmq2mqtt(userClient, bindAddress)
