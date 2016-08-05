import clearblade
from clearblade import auth
from clearblade import Client
from clearblade import Messaging
import time

auth = auth.Auth()

userClient = Client.UserClient("SYSTEM_KEY", "SYSTEM_SECRET", "USER_EMAIL", "USER_PASSWORD", "PLATFORM_URL")
auth.Authenticate(userClient)

message = Messaging.Messaging(userClient)
message.printValue()
message.InitializeMQTT()

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
