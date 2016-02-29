import clearblade
from clearblade import auth
from clearblade import Client
from clearblade import Messaging
import time

auth = auth.Auth()

# userClient = Client.UserClient("8a83d9ec0a8aae92fba990ac9521", "8A83D9EC0AC2A38CAED8CFC6DFA101", "test@clearblade.com", "clearblade", "https://sandbox.clearblade.com") 
userClient = Client.UserClient("eeccc5eb0af8d5e6b5a4c094a474", "EECCC5EB0A90EBC6E09CEE95E65D", "test@clearblade.com", "rohanbendre", "https://rtp.clearblade.com")
auth.Authenticate(userClient)

message = Messaging.Messaging(userClient)
message.printValue()
message.InitializeMQTT(60)

i=0
time.sleep(5)
while i<100:
	message.publishMessage("weather", "Sending message" + str(i+1), 1)
	time.sleep(1)
	i = i+1
	if i == 50:
		print "Waiting 2 minutes"
		time.sleep(90)