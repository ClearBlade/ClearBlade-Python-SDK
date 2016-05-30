import clearblade
from clearblade import auth
from clearblade import Client
from clearblade import Messaging
import time

auth = auth.Auth()

userClient = Client.UserClient("c6d3afec0aa2c4a9dddae6fc899e01", "C6D3AFEC0AC2A59AF5B8FACB8CAE01", "test@clearblade.com", "clearblade", "https://platform.clearblade.com") 
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
while i<20:
	message.publishMessage("weather", "Sending message" + str(i+1), 1)
	time.sleep(1)
	i = i+1
	if i == 10:
		print "Waiting 2 minutes"
		time.sleep(60)
	message.publishMessage("weather", "Sending message" + str(i+1), 1)	