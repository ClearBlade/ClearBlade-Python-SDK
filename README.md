ClearBlade-Python-SDK
==========

A Python SDK for interacting with the ClearBlade Platform.

Python 2 and 3 are supported, but all examples written here are in Python 2.

**Note: This SDK is for use with ClearBlade IoT Enterprise and NOT ClearBlade IoT Core. The Python SDK for ClearBlade IoT Core can be found here: https://github.com/ClearBlade/python-iot.**

## Installation

### To install:
1. Run `pip install clearblade`.
   If you get a permissions error, run `sudo -H pip install clearblade`.
2. If you are on Mac, you may need to update your SSL libraries. 
   If your connections are failing, try: `sudo pip install ndg-httpsclient pyasn1 --upgrade --ignore-installed six`.

### To install from source:
1. Clone or download this repo onto your machine.
2. Run `python setup.py install`.
   This may require additional privileges. 
   If it complains, run again with `sudo -H`.
3. If you are on Mac, you may need to update your SSL libraries. 
   If your connections are failing, try: `sudo pip install ndg-httpsclient pyasn1 --upgrade --ignore-installed six`.

### To install for development (of the SDK):
1. Clone or download this repo onto your machine.
2. Run `python setup.py develop`. 
   This creates a folder called ClearBlade.egg-info in your current directory. 
   You will now be allowed to import the SDK _in the current directory_, and any changes you make to the SDK code will automatically be updated in the egg.

## Usage
1. [Introduction](#introduction)
2. [Systems](#systems)
3. [Users](#users)
4. [Devices](#devices)
5. [Data collections](#data-collections)
6. [MQTT messaging](#mqtt-messaging)
7. [Code services](#code-services)
8. [Queries](#queries)
9. [Developers](#developer-usage)
10. [Advanced](#advanced-usage)

---
### Introduction
The intended entry point for the SDK is the ClearBladeCore module. 
The beginning of your Python file should always include a line like the following:

```python
from clearblade.ClearBladeCore import System, Query, Developer
```

System, Query, and Developer are the only three classes you need to import directly into your project. However, Query and Developer are only used in special situations. 
To register a developer, you must also import the `registerDev` function from ClearBladeCore.

By default, we enable verbose console output. 
If you want your script to be quiet, you can disable the logs by importing the `cbLogs` module and setting the `DEBUG` and `MQTT_DEBUG` flags to `False`. 
Errors will always be printed, even if the debug flags are set to false. 

```python
from clearblade.ClearBladeCore import cbLogs

# Disable console logging
cbLogs.DEBUG = False
cbLogs.MQTT_DEBUG = False
```
**NOTE:**

If you want output of messages to be controlled by python's logging module, set the `cbLogs.USE_LOGS = True`. The MQTT messages are written to the `Mqtt` named logger and `CB` logs are written to the `CB` named logger. So for a configuration that outputs all debug information via the standard library logging module, use:

```python
from clearblade.ClearBladeCore import cbLogs

# logging via the standard logging module
cbLogs.DEBUG = True
cbLogs.MQTT_DEBUG = True
cbLogs.USE_LOGS = True
```

---
### Systems
On the ClearBlade Platform, you develop IoT solutions through **systems**. 
Systems are identified by their SystemKey and SystemSecret. 
These are the only two parameters needed to work with your system. 

By default, we assume your system lives on our public domain: "https&#8203;://platform.clearblade.com". 
If your system lives elsewhere, you can pass the url as the optional third parameter named `url`.

Also, by default, we automatically log out any users you authenticate when your script exits. 
We wrote it this way to reduce the number of user tokens produced from running a script repeatedly. 
However, we realize there are legitimate use cases of wanting to keep users logged in. 
You can turn off this functionality by passing the boolean `False` as the optional fourth parameter named `safe`.

> Definition: `System(systemKey, systemSecret, url="https://platform.clearblade.com", safe=True)`  
> Returns: System object.

#### Examples
A regular system on the ClearBlade Platform.

```python
from clearblade.ClearBladeCore import System

# System credentials
SystemKey = "9abbd2970baabf8aa6d2a9abcc47"
SystemSecret = "9ABBD2970BA6AABFE6E8AEB8B14F"

mySystem = System(SystemKey, SystemSecret)
```
A system hosted on a customer platform, such as https&#8203;://customer.clearblade.com

```python
from clearblade.ClearBladeCore import System

# System credentials
SystemKey = "9abbd2970baabf8aa6d2a9abcc47"
SystemSecret = "9ABBD2970BA6AABFE6E8AEB8B14F"
url = "https://customer.clearblade.com"

mySystem = System(SystemKey, SystemSecret, url)
```

A system hosted on a customer platform with the auto-logout disabled.

```python
from clearblade.ClearBladeCore import System

# System credentials
SystemKey = "9abbd2970baabf8aa6d2a9abcc47"
SystemSecret = "9ABBD2970BA6AABFE6E8AEB8B14F"
url = "https://customer.clearblade.com"

mySystem = System(SystemKey, SystemSecret, url, safe=False)
```
---
### Users
You may have **user** accounts within your system that can perform actions. 

Users can be authenticated in two ways:
1. With their credentials, i.e., email and password. 
2. Without credentials, i.e., anonymously.

> Definition: `System.User(email, password)`  
> Returns: Regular User object.

> Definition: `System.AnonUser()`  
> Returns: Anonymous User object.


Previously authenticated users can also connect to your system without being re-authenticated as long as they provide a valid authToken:

> Definition: `System.User(email, authToken="<valid authToken>")`
> Returns: Regular user object.


Service users (Users that were created with authTokens that are indefinitely valid) can connect to your system as follows:

> Definition: `System.ServiceUser()`  
> Returns: Service user object.

If you allow users to register new user accounts, we have a method for that too. 
You need to authenticate as a user with permission to use one of the functions defined above. 
Then you can register a new user with their email and password. 
This authenticated user may also be a device or developer.

> Definition: `System.registerUser(authenticatedUser, email, password)`  
> Returns: Regular User object.

#### Examples
Authenticating a user.

```python
from clearblade.ClearBladeCore import System

# System credentials
SystemKey = "9abbd2970baabf8aa6d2a9abcc47"
SystemSecret = "9ABBD2970BA6AABFE6E8AEB8B14F"

mySystem = System(SystemKey, SystemSecret)

# Rob's credentials
email = "rob@clearblade.com"
password = "r0s3s"

# Auth as Rob
rob = mySystem.User(email, password)
```
Using an anonymous user to register a new user.

```python
from clearblade.ClearBladeCore import System

# System credentials
SystemKey = "9abbd2970baabf8aa6d2a9abcc47"
SystemSecret = "9ABBD2970BA6AABFE6E8AEB8B14F"

mySystem = System(SystemKey, SystemSecret)

# Auth as anon
anon = mySystem.AnonUser()

# Use the anon user to register Martin
martin = mySystem.registerUser(anon, "martin@clearblade.com", "aQu3m1n1")
```

Using a service user.

```python
from clearblade.ClearBladeCore import System

# System credentials
SystemKey = "9abbd2970baabf8a6d2a9abcc47"
SystemSecret = "9ABBD2970BA6ABFE6E8AEB8B14F"

mySystem = System(SystemKey, SystemSecret)

# Service user
email = "rob@clearblade.com"
token = "yIaddmF42rzKsswf1T7NFNCh9ayg2QQECHRRnbmQfPSdfdaTnw4oWQXmRtv6YoO6oFyfgqq"

# Auth as service user
service_user = mySystem.ServiceUser(email, token)
```
---
### Devices
Another common entity that may interact with your system is a **device**. 
Similar to users, devices must be authenticated before you can use them.

One way to authenticate a device is using its _active key_. 

> Definition: `System.Device(name, key)`  
> Returns: Device object.


Another way to authenticate a device is using mTLS authentication, which requires passing an _x509keyPair_ when creating the device object. 

> Definition: `System.Device(name, x509keyPair={"certfile": "/path/to/your/cert.pem", "keyfile": "/path/to/your.key"})`
> Returns: Device object.

mTLS authentication is achieved by a POST request being sent to API `{platformURL}:444/api/v/4/devices/mtls/auth` with the provided x509keyPair being loaded into the SSL context's cert chain. The SDK handles this.


Previously authenticated devices can also connected to your system without being re-authenticated as long as they provide a valid authToken:

> Definition: `System.Device(name, authToken="<valid authToken>")`
> Returns: Device object.


Want to get a list of all the devices an authenticated entity (user, device, or developer) can view?
You can query those devices with the optional second parameter called `query`. 
For more information on this functionality, see [Queries](#queries).

> Definition: `System.getDevices(authenticatedUser, query=None)`  
> Returns: Device list. Each device is a dictionary of its attributes. 

Only interested in a single device's information? 
If an authenticated user has permission to read its attributes and knows its name, we can do that. 

> Definition: `System.getDevice(authenticatedUser, name)`   
> Returns: A dictionary of the requested device's attributes.

Once you authorize a device through the `System.Device` module, you can update its attributes by passing a JSON blob or a dictionary to the `update` function.

> Definition: `Device.update(info)`  
> Returns: Nothing.

#### Examples
Updating a device's state.

```python
from clearblade.ClearBladeCore import System

# System credentials
SystemKey = "9abbd2970baabf8aa6d2a9abcc47"
SystemSecret = "9ABBD2970BA6AABFE6E8AEB8B14F"

mySystem = System(SystemKey, SystemSecret)

# BLE device's credentials
name = "BLE1"
activeKey = "ATL13ns"

ble = mySystem.Device(name, activeKey)
ble.update({"state": "ON"})
```
---
### Data collections
Every system has an internal database with tables called **collections**. 
You need to be an authenticated user to access them. You must identify them by their _name_ or _id_. 

> Definition: `System.Collection(authenticatedUser, collectionID="", collectionName="")`  
> Returns: Collection object.

Fetching items from your collection can be done through the `getItems` function. 
This function has three optional parameters you can add: 
`query` allows you to only search for certain items (see [Queries](#queries)), 
`pagesize` lets you choose the maximum number of rows to return at once, and 
`pagenum` will request a specific page if there are multiple. 
`url` is an internal parameter and should not be used. 

> Definition: `Collection.getItems(query=None, pagesize=100, pagenum=1, url="")`  
> Returns: List of rows that match your query. Each row is a dictionary of its column values.

Once you fetch items, they get stored in a collection attribute called `items`. 
We also store information about your last request with that collection object to simplify multipage data parsing. 
We have a function to fetch your last request's next and previous pages, which updates the collection's `items` attribute.

> Definition: `Collection.getNextPage()`  
> Returns: List rows from your last request's next page.

> Definition: `Collection.getPrevPage()`  
> Returns: List of rows from the previous page of your last request.

#### Examples
Iterate through the collection's first page.

```python
from clearblade.ClearBladeCore import System

# System credentials
SystemKey = "9abbd2970baabf8aa6d2a9abcc47"
SystemSecret = "9ABBD2970BA6AABFE6E8AEB8B14F"

mySystem = System(SystemKey, SystemSecret)

# Log in as Clark
clark = mySystem.User("clark@clearblade.com", "h00t13h00")

# Clark accesses the collection carolines_guys
myCol = mySystem.Collection(clark, collectionName="carolines_guys")
rows = myCol.getItems()

# Iterate through rows and display them
for row in rows:
    print row
```
---
### MQTT messaging
Every system has a **messaging** client you can use to communicate between authenticated entities (devices, users, edges, developers, platforms, and so on) using the MQTT protocol. 
To become an MQTT client, you only need an authenticated entity (user, device, or developer). 
If your MQTT broker uses a different port from the default (1883), you can set it with the optional second parameter `port`. 
The default keep-alive time is 30 seconds, but you can change that with the optional third parameter, `keepalive`. 
If your broker lives at a different url than your system, you can specify that with the optional fourth parameter `url`. 
You can specify the client_id your script will connect to the broker using the optional fifth parameter `client_id`.
If you don't specify a client_id, the SDK will use a random hex string.

> Definition: `System.Messaging(user, port=1883, keepalive=30, url="", client_id="")`   
> Returns: MQTT messaging object.

There are a number of callback functions you may assign. 
Typically, you want to set these callbacks before you connect to the broker. 
This is a list of the function names and their expected parameters. 
For more information about the individual callbacks, see the [paho-mqtt](https://github.com/eclipse/paho.mqtt.python#callbacks) documentation.   
- `on_connect(client, userdata, flags, rc)`   
- `on_disconnect(client, userdata, rc)`   
- `on_subscribe(client, userdata, mid, granted_qos)`   
- `on_unsubscribe(client, userdata, mid)`   
- `on_publish(client, userdata, mid)`   
- `on_message(client, userdata, mid)`   
- `on_log(client, userdata, level, buf)`   

#### Connecting and Disconnecting
Before publishing or subscribing, you must connect your client to the broker. 
After you're finished, it's good practice to disconnect from the broker before quitting your program. 
These are both simple functions that take no parameters.

> Definition: `Messaging.connect()`   
> Returns: Nothing.   
> Definition: `Messaging.disconnect()`   
> Returns: Nothing.   

#### Last Will and Testament (LWT)
MWTT brokers support the concept of a last will and testament. The last will and testament is a set of parameters that allow the MQTT broker 
publish a specified message to a specific topic in the event of an abnormal disconnection. Setting the last will and testament can be accomplished
by invoking the `set_will` function. The last will and testament can also be removed from a MQTT client by invoking `clear_will`.

**Note: set_will() and clear_will() must be invoked prior to invoking Messaging.connect()**

- `set_will(topic, payload, qos, retain)`   
- `clear_will()`   

> Definition: `Messaging.set_will()`   
> Returns: Nothing.   
> Definition: `Messaging.clear_will()`   
> Returns: Nothing. 


#### Subscribing to topics
You can subscribe to as many topics as you like and unsubscribe from them using the following two commands. 

> Definition: `Messaging.subscribe(topic)`   
> Returns: Nothing.   
> Definition: `Messaging.unsubscribe(topic)`   
> Returns: Nothing.

#### Publishing to topics
Publishing takes the topic to publish to and the message to publish as arguments. The type of message can be string or bytes.

> Definition: `Messaging.publish(topic, message)`   
> Returns: Returns an MQTTMessageInfo, which exposes the following attributes and methods:

1. **rc**, the result of the publishing. It could be MQTT_ERR_SUCCESS to indicate success, MQTT_ERR_NO_CONN if the client is not currently connected, or MQTT_ERR_QUEUE_SIZE when max_queued_messages_set is used to indicate that message is neither queued nor sent.

2. **mid** is the message ID for the publish request. The mid value can be used to track the publish request by checking against the mid argument in the on_publish() callback if it is defined. wait_for_publish may be easier depending on your use-case.

3. **wait_for_publish()** will block until the message is published. It will raise ValueError if the message is not queued (rc == MQTT_ERR_QUEUE_SIZE), or a RuntimeError if there was an error when publishing, most likely due to the client not being connected.

4. **is_published()** returns True if the message has been published. It will raise ValueError if the message is not queued (rc == MQTT_ERR_QUEUE_SIZE), or a RuntimeError if there was an error when publishing, most likely due to the client not being connected.

A ValueError will be raised if the topic is None, has zero length, is invalid (contains a wildcard), QoS is not one of 0, 1, or 2, or the payload length is greater than 268435455 bytes.

#### Examples
Subscribe to the topic and print incoming messages.

```python
from clearblade.ClearBladeCore import System
import time

# System credentials
SystemKey = "9abbd2970baabf8aa6d2a9abcc47"
SystemSecret = "9ABBD2970BA6AABFE6E8AEB8B14F"

mySystem = System(SystemKey, SystemSecret)

# Log in as Sanket
sanket = mySystem.User("sanket@clearblade.com", "SpottieOttieDopaliscious")

# Use Sanket to access a messaging client
mqtt = mySystem.Messaging(sanket)

# Set up callback functions
def on_connect(client, userdata, flags, rc):
    # When we connect to the broker, subscribe to the southernplayalisticadillacmuzik topic
    client.subscribe("southernplayalisticadillacmuzik")
    
def on_message(client, userdata, message):
    # When we receive a message, print it out
    print "Received message '" + message.payload + "' on topic '" + message.topic + "'"
    
# Connect callbacks to client
mqtt.on_connect = on_connect
mqtt.on_message = on_message

# Connect and wait for messages
mqtt.connect()
while(True):
    time.sleep(1)  # wait for messages
```
Publish messages to a topic.

```python
from clearblade.ClearBladeCore import System
import random, time

# System credentials
SystemKey = "9abbd2970baabf8aa6d2a9abcc47"
SystemSecret = "9ABBD2970BA6AABFE6E8AEB8B14F"

mySystem = System(SystemKey, SystemSecret)

# Log in as Adam
adam = mySystem.User("adam@clearblade.com", "a13st0rm")

# Use Adam to access a messaging client
mqtt = mySystem.Messaging(adam)

# Connect 
mqtt.connect()

# When we connect to the broker, start publishing our data to the keelhauled topic
for i in range(20):
    if i%2==0:
        payload = "yo"
    else:
        payload = "ho"
    mqtt.publish("keelhauled", payload)
    time.sleep(1)

mqtt.disconnect()
```
---
### Code services
Within your system, you may have **code services**. 
These JavaScript methods run on the ClearBlade Platform rather than locally.
To use a code service, all you need is its name.

> Definition: `System.Service(name)`   
> Returns: Code service object.

Once you have a code object, you can execute it manually as an authenticated entity (user, device, or developer). 
If you want to pass the service parameters, you can pass them as a dictionary to the optional second parameter, `params`. 

> Definition: `Service.execute(authenticatedUser, params={}`   
> Returns: Response from code service.

#### Examples
Execute a code service with parameters.

```python
from clearblade.ClearBladeCore import System

# System credentials
SystemKey = "9abbd2970baabf8aa6d2a9abcc47"
SystemSecret = "9ABBD2970BA6AABFE6E8AEB8B14F"

mySystem = System(SystemKey, SystemSecret)

# Log in as Aaron
aaron = mySystem.User("aaron@clearblade.com", "Ms_J@cks0n")

# Prepare the gasolineDreams code service
code = mySystem.Service("gasolineDreams")

# Execute the service as Aaron
params = {
    "so_fresh": "so_clean"
}
code.execute(aaron, params)
```
---
### Queries
When you fetch data from collections or devices from the device table, you can get more specific results with a **query**. 
Note: you must import this module from clearblade.ClearBladeCore, separately from the system module.

> Definition: `Query()`   
> Returns: Query object.

Query objects are built through several function calls to narrow your search gradually.
Each operator function takes the column name you're limiting as its first parameter and the value you want to limit by as its second.
The operator functions don't return anything, and they change the query object itself. 
Applying multiple filters to the same query object is logically ANDing them together. 
The `matches` operator matches a regular expression.

* `Query.equalTo(column, value)`
* `Query.greaterThan(column, value)`
* `Query.lessThan(column, value)`
* `Query.greaterThanEqualTo(column, value)`
* `Query.lessThanEqualTo(column, value)`
* `Query.notEqualTo(column, value`
* `Query.matches(column, value)`

If you want to logically OR two queries together, you can pass one to the `Or` function. 
You cannot add more operators through the previous functions once you OR two queries together. 
However, you may OR as many queries together as you'd like.

> Definition: `Query.Or(query)`   
> Returns: New query object representing a logical OR of the filters applied to the original two query objects.

#### Examples
Querying a data collection.

```python
from clearblade.ClearBladeCore import System, Query

# System credentials
SystemKey = "9abbd2970baabf8aa6d2a9abcc47"
SystemSecret = "9ABBD2970BA6AABFE6E8AEB8B14F"

mySystem = System(SystemKey, SystemSecret)

# Log in as Michael
michael = mySystem.User("michael@clearblade.com", "sk3wIt0nTh3B@r-B")

# Michael accesses the collection OutKast_Songs
songs = mySystem.Collection(michael, collectionName="OutKast_Songs")

# We only want songs from the album Aquemini, with a song length between 180-220 seconds
q = Query()
q.equalTo("album", "Aquemini")
q.greaterThan("song_length", 180)
q.lessThat("song_length", 220)

# Fetch rows that fit our query filters
rows = myCol.getItems(q)

# Iterate through rows and display them
for row in rows:
    print row
```
Querying the device table.

```python
from clearblade.ClearBladeCore import System

# System credentials
SystemKey = "9abbd2970baabf8aa6d2a9abcc47"
SystemSecret = "9ABBD2970BA6AABFE6E8AEB8B14F"

mySystem = System(SystemKey, SystemSecret)

# Log in as Jim
jim = mySystem.User("jim@clearblade.com", "r3turn0fTh3_G_")

# We only want active BLE *or* active Zigbee devices
q = Query()
q.equalTo("type", "BLE")
q.equalTo("state", "active")

q2 = Query()
q2.equalTo("type", "Zigbee")
q2.equalTo("state", "active")

# Fetch devices that fit our query filters
devices = mySystem.getDevices(jim, q.Or(q2))

# Print results
for device in devices:
    print device
```
## Developer usage
Developer usage is not fully implemented yet and is currently restricted to the following classes:

1. [Devices](#devices-1)

**Developers** have less restricted access to your system's components. 
However, developer functionality is not object-oriented. 
Additionally, since a developer may have multiple systems, most functions require you to pass in a [System](#systems) object. 

You can register yourself from the SDK if you're not a developer. 
You need the typical credentials: first name, last name, organization, email, and password. 
You must import this function directly from `clearblade.ClearBladeCore`.

By default, we assume you're registering on our public domain: "https&#8203;://platform.clearblade.com". 
If you're registering elsewhere, you can pass the url as the optional sixth parameter named `url`.

> Definition: `registerDev(fname, lname, org, email, password, url="https://platform.clearblade.com")`   
> Returns: Developer object.

You can log in with your email and password if you're already a registered developer with the Platform. 
Like the registration function, if you're logging into an account on a different domain than the default, you can pass it in as the optional third parameter named `url`. 

> Definition: `Developer(email, password, url="https://platform.clearblade.com")`   
> Returns: Developer object.

When you create your developer object, you will be automatically authenticated. 
You can log out and authenticate yourself again as often as possible with the aptly named functions below.

> Definition: `Developer.logout()`   
> Returns: Nothing.
> 
> Definition: `Developer.authenticate()`   
> Returns: Nothing.

#### Examples
Register a developer.

```python
from clearblade.ClearBladeCore import registerDev

# Andre's credentials
first_name = "Andre"
last_name = "3000"
organization = "OutKast"
email = "andre.l.benjamin@outkast.com"
password = "h3y_y@!"

# Register Andre with the ClearBlade Platform
andre = registerDev(first_name, last_name, organization, email, password)
```

Log in as a developer.

```python
from clearblade.ClearBladeCore import Developer

# Log in as Big Boi
bigboi = Developer("antwan.a.patton@outkast.com", "th3w@yY0uM0v3")
```
---
### Collections
First, you can get a list of all current collections within a system.

> Definition: `Developer.getAllCollections(system)`  
> Returns: List of collections. Each collection is a dictionary containing the collection name and collectionID.  

As a developer, you get full management access to any collection within a system. To create a cloud collection, specify the system it will live in and your new collection name.

> Definition: `Developer.newCollection(system, name)`  
> Returns: A collection object of the newly created collection

You can also add columns to any collection. The collection object you supply should be initialized with a `collectionID` (rather than `collectionName`) to add columns. The collection object returned from `Developer.newCollection` is initialized this way for you for ease of use.

> Definition: `Developer.addColumnToCollection(system, collectionObject, columnName, columnType)`  
> Returns: Nothing

Finally, you can set the CRUD permissions for a collection via a specific role name. Like `addColumnToCollection`, you will need to use a collection object initialized with a `collectionID`.

> Definition: `Developer.setPermissionsForCollection(system, collectionObject, Permissions.READ + Permissions.UPDATE, roleName)`  
> Returns: Nothing

#### Examples
Creating a new collection and adding a custom column.

```python
from clearblade.ClearBladeCore import System, Developer

# System credentials
SystemKey = "9abbd2970baabf8aa6d2a9abcc47"
SystemSecret = "9ABBD2970BA6AABFE6E8AEB8B14F"

mySystem = System(SystemKey, SystemSecret)

# Log in as Steve
steve = Developer("steve@clearblade.com", "r0s@_p@rks")

# Create new Collection named Tools
toolsCollection = steve.newCollection(mySystem, "Tools")

# Add a column to the collection called last_location with a type of string
steve.addColumnToCollection(mySystem, toolsCollection, "last_location", "string")
```

Updating CRUD permissions for a collection on a specific role.

```python
from clearblade.ClearBladeCore import System, Developer, Collections, Permissions

# System credentials
SystemKey = "9abbd2970baabf8aa6d2a9abcc47"
SystemSecret = "9ABBD2970BA6AABFE6E8AEB8B14F"

mySystem = System(SystemKey, SystemSecret)

# Log in as Steve
steve = Developer("steve@clearblade.com", "r0s@_p@rks")

# Create a collection object from an existing collection with an id of 8a94dda70bb4c2c59b8298d686f401
collectionObj = mySystem.Collection(steve, collectionID="8a94dda70bb4c2c59b8298d686f401")

# Give the authenticated role read and delete permissions to this collection
michael.setPermissionsForCollection(mySystem, collectionObj, Permissions.READ + Permissions.DELETE, "Authenticated")
```

---
### Devices
As a developer, you get full CRUD access to the device table. 

To create a device, specify the system it will live in and the device name you're creating. 
There are many other optional parameters you may set, but all have default values. 
You should keep enabled set to true and allow at least one type of authentication if you want to interact with the device through the non-developer endpoints.

> Definition: `Developer.newDevice(system, name, enabled=True, type="", state="", active_key="", allow_certificate_auth=False, allow_key_auth=True, certificate="", description="", keys="")`   
> Returns: Dictionary of the new device's attributes.

You can get a full list of devices in your system's device table and [query](#queries) it. 
You can ask for that device by name if you have a specific device you want information about. 

> Definition: `Developer.getDevices(system, query=None)`   
> Returns: Device list. Each device is a dictionary of its attributes.

> Definition: `Developer.getDevice(system, name)`   
> Returns: Dictionary of the requested device's attributes.

Updating a device takes the system object, device name, and dictionary of the updates you are making. 

> Definition: `Developer.updateDevice(system, name, updates)`   
> Returns: Dictionary of the updated device's attributes.

Deleting a device is as simple as passing in the system object where it lives and the device name. 

> Definition: `Developer.deleteDevice(system, name)`   
> Returns: Nothing.

#### Examples
Creating and updating a device.

```python
from clearblade.ClearBladeCore import System, Developer

# System credentials
SystemKey = "9abbd2970baabf8aa6d2a9abcc47"
SystemSecret = "9ABBD2970BA6AABFE6E8AEB8B14F"

mySystem = System(SystemKey, SystemSecret)

# Log in as Steve
steve = Developer("steve@clearblade.com", "r0s@_p@rks")

# Create new a device named Elevators
steve.newDevice(mySystem, "Elevators")

# Update device description
steve.updateDevice(mySystem, "Elevators", {"description": "(Me & You)"})
```
Getting device information and deleting a device.

```python
from clearblade.ClearBladeCore import System, Developer

# System credentials
SystemKey = "9abbd2970baabf8aa6d2a9abcc47"
SystemSecret = "9ABBD2970BA6AABFE6E8AEB8B14F"

mySystem = System(SystemKey, SystemSecret)

# Log in as Kevin
devKev = Developer("kevin@clearblade.com", "j@zZy_b3ll3")

# Get device named TwoDopeBoyz
tdb = devKev.getDevice(mySystem, "TwoDopeBoyz")

# Conditional delete
if tdb["description"] != "(In a Cadillac)":
    devKev.deleteDevice(mySystem, "TwoDopeBoyz")
```
---
## Advanced usage

### SSL verification
If you need to disable SSL verification (likely in the case of a self-signed SSL certificate), initialize a system, and include a `sslVerify=True` parameter.

#### Examples
```python
from clearblade.ClearBladeCore import System

# System credentials
SystemKey = "9abbd2970baabf8aa6d2a9abcc47"
SystemSecret = "9ABBD2970BA6AABFE6E8AEB8B14F"
url = "https://customer.clearblade.com"

mySystem = System(SystemKey, SystemSecret, url, sslVerify=False)
```

**Note** This option should only be enabled when using a ClearBlade Platform instance with a self-signed SSL certificate. If your instance uses a valid SSL certificate signed with a known CA, you should **not** enable this.
