Python-API
==========

A python API for interacting with the ClearBlade Platform


Clone the repository from https://github.com/ClearBlade/Python-API

From inside the folder, install the sdk using - sudo python setup.py install

Sample programs are provided in SampleCodes folder

USAGE:

# Auth as user

userClient = Client.UserClient(SYS_KEY, SYS_SECRET, USER_EMAIL, PASSWORD)
auth = Auth()
auth.Authenticate(userClient)

# Auth as developer

devClient = Client.DevClient(SYS_KEY, SYS_SECRET, DEV_EMAIL, PASSWORD)
auth.Authenticate(devClient)


# Create Messaging object as user

message = Messaging.Messaging(userClient)

# Init and connect to mqtt broker

message.InitializeMQTT()

# Publish messages

message.publishMessage("weather", "Testing", 0)

# Subscribe to topic

message.subscribe("weather", 0)

# Execute code service

params = {"city" : "Austin"}
code = Code.CodeService(userClient)
code.CallService("ServicePart4", params, "false")
