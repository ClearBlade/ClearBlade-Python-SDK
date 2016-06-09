import zmq
import time
import clearblade
from clearblade import auth
from clearblade import Client
from clearblade import Messaging

class pub():

	def zmqSend(self, data, bindAddress):
		#bindAddress = "tcp://127.0.0.1:7777"
		print "data is "+data
		# ZeroMQ Context
		context = zmq.Context()

		# Define the socket using the "Context"
		sock = context.socket(zmq.PUB)
		print "Bind Address is "+bindAddress
		sock.bind(bindAddress)

		time.sleep(1)
		data, now = data, time.ctime()
		# Message [prefix][message]
		message = "1#"+data
		sock.send(message)
