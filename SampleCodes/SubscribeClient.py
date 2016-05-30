import clearblade
from clearblade import auth
from clearblade import Client
from clearblade import Messaging
import time

auth = auth.Auth()

userClient = Client.UserClient("c6d3afec0aa2c4a9dddae6fc899e01", "C6D3AFEC0AC2A59AF5B8FACB8CAE01", "test@clearblade.com", "clearblde", "https://platform.clearblade.com") 

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

message.subscribe("weather", 1)
time.sleep(5)
count = 0
while count < 20:
	count = count + 1
	time.sleep(1)
	if count == 10:
		print "Waiting 2 minutes"
		time.sleep(60)
		message.subscribe("weather", 1)