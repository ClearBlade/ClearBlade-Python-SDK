import paho.mqtt.client as mqtt
import thread
import time
import Client
import UserClient 
import string
import auth
import Messaging
import zmq

class mqtt2zmq():

	def __init__(self, userClient, bindAddress):
		self.userClient = userClient
		self.bindAddress = bindAddress
		self.auth = auth.Auth()
		self.auth.Authenticate(self.userClient)
		self.message = Messaging.Messaging(self.userClient)
		self.message.printValue()
		self.status = self.message.InitializeMQTT(keep_alive=60)
		context = zmq.Context()

		# Define the socket using the "Context"
		self.sock = context.socket(zmq.PUB)
		print "Bind Address is "+bindAddress
		self.sock.bind(bindAddress)
		self.mqttSub(self.message,self.sock)

	def mqttSub(self, message, sock):
		time.sleep(1)

		def onMessageCallback(client, obj, msg):
			print "Your message is : "+msg.payload
			data = msg.payload
			self.ZmqPub(data, self.sock)



		message.subscribe("zmq/subscribe", 1, onMessageCallback)
		while True:
			pass

	def ZmqPub(self, data, sock):
		time.sleep(1)
		message = "1#"+data
		self.sock.send(message)

if __name__ == '__main__':
	userClient = Client.UserClient("cecdeef40a98c1e1cb87c58dad58", "CECDEEF40A869A818AC6D9D4C21F", "parent@acme.com", "edge", "http://localhost") 
	bindAddress = "tcp://127.0.0.1:7777"
	mqtt2zmq = mqtt2zmq(userClient, bindAddress)