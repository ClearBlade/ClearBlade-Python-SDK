import clearblade
from clearblade import auth
from clearblade import Client
from clearblade import Messaging
import time

auth = auth.Auth()

# userClient = Client.UserClient("8a83d9ec0a8aae92fba990ac9521", "8A83D9EC0AC2A38CAED8CFC6DFA101", "testcb@clearblade.com", "clearblade", "https://sandbox.clearblade.com")

userClient = Client.UserClient("eeccc5eb0af8d5e6b5a4c094a474", "EECCC5EB0A90EBC6E09CEE95E65D", "register@clearblade.com", "clearblade", "https://rtp.clearblade.com")
auth.Authenticate(userClient)

message = Messaging.Messaging(userClient)
message.printValue()
message.InitializeMQTT(60)

message.subscribe("weather", 1)
time.sleep(5)
count = 0
while count < 100:
	count = count + 1
	time.sleep(1)
	if count == 50:
		print "Waiting 2 minutes"
		time.sleep(90)
		message.subscribe("weather", 1)