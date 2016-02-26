import auth
import Client
import Messaging
import time

auth = auth.Auth()

# userClient = Client.UserClient("8c8e98e20af4d8d5f8b884f2fbe301", "8C8E98E20AA6818AD49099AFF29901", "subscribe@clearblade.com", "clearblade")
userClient = Client.UserClient("eeccc5eb0af8d5e6b5a4c094a474", "EECCC5EB0A90EBC6E09CEE95E65D", "subscribe@clearblade.com", "clearblade")
auth.Authenticate(userClient)

message = Messaging.Messaging(userClient)
message.printValue()
message.InitializeMQTT()

message.subscribe("weather", 1)
time.sleep(5)
count = 0
while count < 5:
	count = count + 1
	time.sleep(2)
