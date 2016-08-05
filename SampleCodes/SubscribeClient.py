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
status = message.InitializeMQTT()

time.sleep(1)
def onMessageCallback(client, obj, msg):
	print "Payload: "+msg.payload

message.subscribe("weather", 1, onMessageCallback)

while True:
	pass




