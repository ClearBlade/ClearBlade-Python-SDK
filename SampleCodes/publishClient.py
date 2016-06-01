import clearblade
from clearblade import auth
from clearblade import Client
from clearblade import Messaging
import time

auth = auth.Auth()

userClient = Client.UserClient("cecdeef40a98c1e1cb87c58dad58", "CECDEEF40A869A818AC6D9D4C21F", "parent@acme.com", "edge", "http://localhost") 
# userClient = Client.UserClient("eeccc5eb0af8d5e6b5a4c094a474", "EECCC5EB0A90EBC6E09CEE95E65D", "test@clearblade.com", "rohanbendre", "https://rtp.clearblade.com")
auth.Authenticate(userClient)

message = Messaging.Messaging(userClient)
message.printValue()
message.InitializeMQTT()


# message.publishMessage("weather", "Sending message", 1)
# message.publishMessage("weather", "Sending message", 1)
# message.publishMessage("weather", "Sending message", 1)
# message.publishMessage("weather", "Sending message", 1)
# message.publishMessage("weather", "Sending message", 1)
# time.sleep(10)
# message.disconnect()
# time.sleep(15)
# message.InitializeMQTT()
# message.publishMessage("weather", "Sending message", 1)
# message.publishMessage("weather", "Sending message", 1)
# message.publishMessage("weather", "Sending message", 1)
# message.publishMessage("weather", "Sending message", 1)
# message.publishMessage("weather", "Sending message", 1)
# time.sleep(45)
# message.publishMessage("weather", "Sending message", 1)
# message.publishMessage("weather", "Sending message", 1)
# message.publishMessage("weather", "Sending message", 1)
# time.sleep(45)
# message.publishMessage("weather", "Sending message", 1)

i=0
time.sleep(5)
while i<100:
	message.publishMessage("weather", "Sending message" + str(i+1), 1)
	time.sleep(1)
	i = i+1
	if i == 10:
		print "Waiting 2 seconds"
		time.sleep(2)
	message.publishMessage("weather", "Sending message" + str(i+1), 1)	
