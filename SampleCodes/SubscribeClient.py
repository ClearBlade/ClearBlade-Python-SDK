import clearblade
from clearblade import auth
from clearblade import Client
from clearblade import Messaging
import time

auth = auth.Auth()

userClient = Client.UserClient("cecdeef40a98c1e1cb87c58dad58", "CECDEEF40A869A818AC6D9D4C21F", "parent@acme.com", "edge", "http://localhost") 

# userClient = Client.UserClient("eeccc5eb0af8d5e6b5a4c094a474", "EECCC5EB0A90EBC6E09CEE95E65D", "register@clearblade.com", "clearblade", "https://rtp.clearblade.com")
auth.Authenticate(userClient)


message = Messaging.Messaging(userClient)
message.printValue()
status = message.InitializeMQTT(keep_alive=60)

print status
if status == 4:
	print "Error in connection.. Aborting!!"
	exit(1)

# time.sleep(5)
# message.subscribe("weather", 1)
# time.sleep(10)
# message.disconnect()
# time.sleep(10)
# message.InitializeMQTT()
# time.sleep(5)
# message.subscribe("weather", 1)
# time.sleep(650)
# print "3"
# time.sleep(650)
# print "4"
# time.sleep(650)
# print "5"
# time.sleep(650)
# print "6"
# time.sleep(650)
# print "7"
# time.sleep(650)

time.sleep(1)
message.subscribe("weather", 1)
message.subscribe("weave",1)
message.subscribe("top",0)
time.sleep(1)
message.unsubscribe("weave")
while True:
	pass




