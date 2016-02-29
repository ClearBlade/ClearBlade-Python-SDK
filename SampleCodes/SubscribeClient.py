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