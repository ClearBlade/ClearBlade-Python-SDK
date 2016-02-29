import clearblade
from clearblade import auth
from clearblade import Client
from clearblade import Messaging
import time

auth = auth.Auth()

userClient = Client.UserClient("SYSKEY", "SYSSECRET", "USER_EMAIL", "PASSWORD", "PLATFORM URL")
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