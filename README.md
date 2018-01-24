ClearBlade-Python-SDK
==========

A Python SDK for interacting with the ClearBlade Platform.

Both Python 2 and 3 are supported, but all examples written here are in Python 2.

## Installation

### To install:
1. Run `pip install clearblade`.
   If you get a permissions error, run `sudo -H pip install clearblade`.
2. If on Mac, you may need to update your SSL libraries. 
   If your connections are failing, try: `sudo pip install ndg-httpsclient pyasn1 --upgrade --ignore-installed six`

### To install from source:
1. Clone or download this repo on to your machine.
2. Run `python setup.py install`.
   This may require additional priviledges. 
   If it complains, run again with `sudo -H`.
3. If on Mac, you may need to update your SSL libraries. 
   If your connections are failing, try: `sudo pip install ndg-httpsclient pyasn1 --upgrade --ignore-installed six`

### To install for development (of the SDK):
1. Clone or download this repo on to your machine.
2. Run `python setup.py develop`. 
   This creates a folder called ClearBlade.egg-info in your current directory. 
   You will now be allowed to import the SDK _in the current directory_, and any changes you make to the SDK code will automatically be updated in the egg.

## Usage
1. [Introduction](#introduction)
1. [Systems](#systems)
1. [Users](#users)
1. [Devices](#devices)
1. [Data Collections](#data-collections)
1. [MQTT Messaging](#mqtt-messaging)
1. [Code Services](#code-services)
1. [Queries](#queries)
1. [Developers](#developer-usage)
1. [Advanced](#advanced-usage)

---
### Introduction
The intended entry point for the SDK is the ClearBladeCore module. 
The beginning of your python file should always include a line like the following:

```python
from clearblade.ClearBladeCore import System, Query, Developer
```

System, Query, and Developer are the only three classes you should ever need to import directly into your project, however Query and Developer are only used in special situations. 
To register a developer, you will also need to import the `registerDev` function from ClearBladeCore.

By default, we enable verbose console output. 
If you want your script to be quiet, you can disable the logs with by importing the `cbLogs` module and setting the `DEBUG` and `MQTT_DEBUG` flags to `False`. 
Note that errors will always be printed, even if the debug flags are set to false. 

```python
from clearblade.ClearBladeCore import cbLogs

# Disable console logging
cbLogs.DEBUG = False
cbLogs.MQTT_DEBUG = False
```
---
### Systems
On the ClearBlade platform, you develop IoT solutions through **Systems**. 
Systems are identified by their SystemKey and SystemSecret. 
These are the only two parameters needed to work with your system. 

By default, we assume your system lives on our public domain: "https&#8203;://platform.clearblade.com". 
If your system lives elsewhere, you can pass the url as the optional third parameter named `url`.

Also by default, we automatically log out any users you authenticate when your script exits. 
We wrote it this way to reduce the number of user tokens being produced from running a script repeatedly. 
However, we realize that there are legitimate use cases of wanting to keep users logged in. 
You can turn off this functionality by passing the boolean `False` as the optional fourth parameter named `safe`.

> Definition: `System(systemKey, systemSecret, url="https://platform.clearblade.com", safe=True)`  
> Returns: System object.

#### Examples
A regular system on the ClearBlade platform.

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
Within your System, you may have **User** accounts that can perform actions. 
Users can be authenticated with their email and password. 
You may also allow for people to authenticate to your system anonymously. 
In this case, no email or password is needed. 

> Definition: `System.User(email, password)`  
> Returns: Regular User object.

> Definition: `System.AnonUser()`  
> Returns: Anonymous User object.

If you allow users to register new user accounts, we have a method for that too. 
You need to first authenticate as a user that has the permissions to do so using one of the functions defined above. 
Then you can register a new user with their email and password. 
Note that this authenticated user may also be a device or developer.

> Defininition: `System.registerUser(authenticatedUser, email, password)`  
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
---
### Devices
Another common entity that may interact with your system is a **Device**. 
Similar to users, devices must be authenticated before you can use them. 
To authenticate a device, you need its _active key_. 

> Definition: `System.Device(name, key)`  
> Returns: Device object.

Want to get a list of all the devices an authenticated entity (user, device, or developer) can view?
Simple. 
We even have a way to query those devices with the optional second parameter called `query`. 
For more information on this functionality, see [Queries](#queries).

> Definition: `System.getDevices(authenticatedUser, query=None)`  
> Returns: List of devices. Each device is a dictionary of their attributes. 

Only interested in a single device's information? 
If an authenticated user has permission to read its attributes and knows its name, we can do that. 

> Definition: `System.getDevice(authenticatedUser, name)`   
> Returns: A dictionary of the requested device's attributes.

Once you authorize a device through the `System.Device` module, you can update its attributes by passing a json blob or a dictionary to the `update` function.

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
### Data Collections
Every system has an internal database with tables called **Collections**. 
You need to be an authenticated user to access them, and you must identify them by either their _name_ or their _id_. 

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

Once you fetch items, they get stored to a collection attribute called `items`. 
We also store some information about your last request with that collection object to make multipage data parsing a little easier. 
We have a function to fetch the next page and the previous page of the last request you made, which update the collection's `items` attribute.

> Definition: `Collection.getNextPage()`  
> Returns: List of rows from the next page of your last request.

> Definition: `Collection.getPrevPage()`  
> Returns: List of rows from the previous page of your last request.

#### Examples
Iterate through first page of a collection.

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
### MQTT Messaging
Every system has a **Messaging** client you can use to communicate between authenticated entities (devices, users, edges, developers, platforms, so on) using the MQTT protocol. 
To become an MQTT client, all you need is an authenticated entity (user, device, or developer). 
If your MQTT broker uses a different port from the default (1883), you can set it with the optional second parameter `port`. 
The default keep-alive time is 30 seconds, but you can change that with the optional third parameter `keepalive`. 
Lastly, if your broker lives at a different url than your system, you can specify that with the optional fourth parameter `url`. 

> Definition: `System.Messaging(user, port=1883, keepalive=30, url="")`   
> Returns: MQTT Messaging object.

There are a slew of callback functions you may assign. 
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

Before publishing or subscribing, you must connect your client to the broker. 
After you're finished, it's good practice to disconnect from the broker before quitting your program. 
These are both simple functions that take no parameters.

> Definition: `Messaging.connect()`   
> Returns: Nothing.   
> Definition: `Messaging.disconnect()`   
> Returns: Nothing.   

You can subscribe to as many channels as you like, and subsequently unsubscribe from them, using the following two commands. 

> Definition: `Messaging.subscribe(channel)`   
> Returns: Nothing.   
> Definition: `Messaging.unsubscribe(channel)`   
> Returns: Nothing.

Lastly, publishing takes the channel to publish to, and the message to publish as arguments. 

> Definition: `Messaging.publish(channel, message)`   
> Returns: Nothing.

#### Examples
Subscribe to channel and print incoming messages.

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
    # When we connect to the broker, subscribe to the southernplayalisticadillacmuzik channel
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
Publish messages to a channel.

```python
from clearblade.ClearBladeCore import System
import random

# System credentials
SystemKey = "9abbd2970baabf8aa6d2a9abcc47"
SystemSecret = "9ABBD2970BA6AABFE6E8AEB8B14F"

mySystem = System(SystemKey, SystemSecret)

# Log in as Adam
adam = mySystem.User("adam@clearblade.com", "a13st0rm")

# Use Adam to access a messaging client
mqtt = mySystem.Messaging(adam)


# Set up callback function
def on_connect(client, userdata, flags, rc):
    # When we connect to the broker, start publishing our data to the keelhauled channel
    for i in range(20):
        if i%2==0:
            payload = "yo"
        else:
            payload = "ho"
        client.publish("keelhauled", payload)
        time.sleep(1)


# Connect callback to client
mqtt.on_connect = on_connect

# Connect and spin for 30 seconds before disconnecting
mqtt.connect()
time.sleep(30)
mqtt.disconnect()
```
---
### Code Services
Within your system, you may have **Code Services**. 
These are javascript methods that are run on the ClearBlade Platform rather than locally. 
To use a code service, all you need is its name.

> Definition: `System.Service(name)`   
> Returns: Code Service object.

Once you have a code object, you can execute it manually as an authenticated entity (user, device, or developer). 
If you want to pass the service parameters, you can pass them as a dictionary to the optional second parameter `params`. 

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
When you fetch data from collections or devices from the device table, you can get more specific results with a **Query**. 
Note: you must import this module from clearblade.ClearBladeCore, seperately from the System module.

> Definition: `Query()`   
> Returns: Query object.

Query objects are built through several function calls to gradually narrow your search down. 
Each operator function takes the column name you're limiting as its first parameter, and the value you want to limit by as its second.
The operator functions don't return anything, they change the query object itself. 
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
Note that once you OR two queries together, you cannot add any more operators through the previous functions. 
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
## Developer Usage
Developer usage is not fully implemented yet and is currently restricted to the following classes:

1. [Devices](#devices-1)

**Developers** have a less restricted access to your system's components. 
However, developer functionality is not object oriented. 
Additionally, since a developer may have multiple systems, most functions will require you to pass in a [System](#systems) object. 

If you're not already a developer, you can register yourself from the SDK. 
You need the typical credentials: first name, last name, organization, email, and password. 
You will have to import this function directly from `clearblade.ClearBladeCore`.

By default, we assume you're registering on our public domain: "https&#8203;://platform.clearblade.com". 
If you're registering elsewhere, you can pass the url as the optional sixth parameter named `url`.

> Definition: `registerDev(fname, lname, org, email, password, url="https://platform.clearblade.com")`   
> Returns: Developer object.

If you're already a registered developer with the platform, you can log in with your email and password. 
Like the registration function, if you're logging into an account on a different domain than the default, you can pass it in as the optional third parameter named `url`. 

> Definition: `Developer(email, password, url="https://platform.clearblade.com")`   
> Returns: Developer object.

When you create your developer object you will be automatically authenticated. 
You may then log out and authenticate yourself again as many times as you like with the aptly named functions below. 

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
### Devices
As a developer, you get full CRUD access to the device table. 

To create a device, you need to specify the system it's going to live in, and the name of the device you're creating. 
There are many other optional parameters that you may set if you please, but all have default values if you're feeling lazy. 
Note: you should keep enabled set to True and allow at least one type of authentication if you want to interact with the device through the non-developer endpoints.

> Definition: `Developer.newDevice(system, name, enabled=True, type="", state="", active_key="", allow_certificate_auth=False, allow_key_auth=True, certificate="", description="", keys="")`   
> Returns: Dictionary of the new device's attributes.

You can get a full list of devices in your system's device table and [query](#queries) it if you'd like. 
If you have a specific device you want information about, you can ask for that device by name. 

> Definition: `Developer.getDevices(system, query=None)`   
> Returns: List of devices. Each device is a dictionary of their attributes.

> Definition: `Developer.getDevice(system, name)`   
> Returns: Dictionary of the requested device's attributes.

Updating a device takes the system object, name of the device, and a dictionary of the updates you are making. 

> Definition: `Developer.updateDevice(system, name, updates)`   
> Returns: Dictionary of the updated device's attributes.

Deleting a device is as simple as passing in the system object where it lives and the name of the device. 

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

# Create new device named Elevators
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
## Advanced Usage

### SSL Verification
If you need to disable SSL verification (likely in the case of a self-signed SSL certificate), you simply need to initialize a System like you normally would, and include a `sslVerify=True` parameter.

#### Examples
```python
from clearblade.ClearBladeCore import System

# System credentials
SystemKey = "9abbd2970baabf8aa6d2a9abcc47"
SystemSecret = "9ABBD2970BA6AABFE6E8AEB8B14F"
url = "https://customer.clearblade.com"

mySystem = System(SystemKey, SystemSecret, url, sslVerify=False)
```

**Note** This option should only be enabled when using a ClearBlade Platform instance with a self-signed SSL certificate. If your instance is using a valid SSL certificate signed with a known CA, you should **not** enable this.
