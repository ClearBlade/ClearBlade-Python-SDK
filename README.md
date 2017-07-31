Python-SDK
==========

A Python SDK for interacting with the ClearBlade Platform.

Both Python 2 and 3 are supported, but all examples written here are in Python 2.

## Installation

### To install for regular use:
1. Clone or download this repo on to your machine.
2. Run `python setup.py install`.

### To install for development (of the sdk):
1. Clone or download this repo on to your machine.
2. Run `python setup.py develop`. This creates a folder called ClearBlade.egg-info in your current directory. You will now be allowed to import the sdk _in the current directory_, and any changes you make to the sdk code will automatically be updated in the egg.

## Usage
The intended entry point for the sdk is the ClearBladeCore module. The beginning of your python file should always include a line like the following:

```python
from clearblade.ClearBladeCore import System, Query, Developer
```

System, Query, and Developer are the only three classes you should ever need to import directly into your project, however Query and Developer are only used in special situations. 

If you want to enable console logging, you must also set the debug flags. The module `cbLogs` has a `DEBUG` flag which enables verbose console messages, and an `MQTT_DEBUG` flag which displays additional logging specifically pertaining to MQTT messaging. 

```python
from clearblade import cbLogs

# Enable console logging
cbLogs.DEBUG = True
cbLogs.MQTT_DEBUG = True
```

### Systems
On the ClearBlade platform, you develop IoT solutions through **Systems**. Systems are identified by their SystemKey and SystemSecret. These are the only two parameters needed to work with your system. 

By default, we assume your system lives on our public domain: "https://platform.clearblade.com". If your system lives elsewhere, you can pass the url as the optional third parameter named `url`.

Also by default, we automatically log out any users you authenticate when your script exits. We wrote it this way to reduce the number of user tokens being produced from running a script repeatedly. However, we realize that there are legitimate use cases of wanting to keep users logged in. You can turn off this functionality by passing the boolean `False` as the optional fourth parameter named `safe`.

> Definition: `System(systemKey, systemSecret, url="https://platform.clearblade.com", safe=True)`  
> Returns: System object.

##### Examples
A regular system on the ClearBlade platform.

```python
from clearblade.ClearBladeCore import System

# System credentials
SystemKey = "9abbd2970baabf8aa6d2a9abcc47"
SystemSecret = "9ABBD2970BA6AABFE6E8AEB8B14F"

mySystem = System(SystemKey, SystemSecret)
```
A system hosted on mydomain.clearblade.com with the auto-logout disabled.

```python
from clearblade.ClearBladeCore import System

# System credentials
SystemKey = "9abbd2970baabf8aa6d2a9abcc47"
SystemSecret = "9ABBD2970BA6AABFE6E8AEB8B14F"
url = "https://mydomain.clearblade.com"

mySystem = System(SystemKey, SystemSecret, url, safe=False)
```

### Users
Within your System, you may have **User** accounts that can perform actions. Users can be authenticated with their email and password. You may also allow for people to authenticate to your system anonymously. In this case, no email or password is needed. 

> Definition: `System.User(email, password)`  
> Returns: Regular User object.

> Definition: `System.AnonUser()`  
> Returns: Anonymous User object.

If you allow users to register new user accounts, we have a method for that too. You need to first authenticate as a user that has the permissions to do so using one of the functions defined above. Then you can register a new user with their email and password. Note that this authenticated user may also be a device or developer.

> Defininition: `System.registerUser(authenticatedUser, email, password)`  
> Returns: Regular User object.

##### Examples
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

### Devices
Another common entity that may interact with your system is a **Device**. Similar to users, devices must be authenticated before you can use them. To authenticate a device, you need its _active key_. 

> Definition: `System.Device(name, key)`  
> Returns: Device object.

Want to get a list of all the devices an authenticated user (or other device, or developer) can view? Simple. We even have a way to query those devices with the optional second parameter called `query`. For more information on this functionality, see [Queries](#queries).

> Definition: `System.getDevices(authenticatedUser, query=None)`  
> Returns: List of devices. Each device is a dictionary of their attributes. 

Only interested in a single device's information? If an authenticated user has permission to read its attributes and knows its name, we can do that. 

> Definition: `System.getDevice(authenticatedUser, name)`   
> Returns: A dictionary of the requested device's attributes.

Once you authorize a device through the `System.Device` module, you can update its attributes by passing a json blob or a dictionary to the `update` function.

> Definition: `Device.update(info)`  
> Returns: Nothing.

##### Examples
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

### Data Collections
Every system has an internal database with tables called **Collections**. You need to be an authenticated user to access them, and you must identify them by either their _name_ or their _id_. 

> Definition: `System.Collection(authenticatedUser, collectionID="", collectionName="")`  
> Returns: Collection object.

Fetching items from your collection can be done through the `getItems` function. This function has three optional parameters you can add: `query` allows you to only search for certain items (see [Queries](#queries)), `pagesize` lets you choose the maximum number of rows to return at once, and `pagenum` will request a specific page if there are multiple. `url` is an internal parameter and should not be used. 

> Definition: `Collection.getItems(query=None, pagesize=100, pagenum=1, url="")`  
> Returns: List of rows that match your query. Each row is a dictionary of its column values.

Once you fetch items, they get stored to a collection attribute called `items`. We also store some information about your last request with that collection object to make multipage data parsing a little easier. We have a function to fetch the next page and the previous page of the last request you made, which update the collection's `items` attribute.

> Definition: `Collection.getNextPage()`  
> Returns: List of rows from the next page of your last request.

> Definition: `Collection.getPrevPage()`  
> Returns: List of rows from the previous page of your last request.

##### Examples
Iterate through first page of a collection.

```python
from clearblade.ClearBladeCore import System

# System credentials
SystemKey = "9abbd2970baabf8aa6d2a9abcc47"
SystemSecret = "9ABBD2970BA6AABFE6E8AEB8B14F"

mySystem = System(SystemKey, SystemSecret)

# Log in as Clark
clark = mySystem.User("clark@clearblade.com", "h00t13h00")

# Clark accesses the collection myCol
myCol = mySystem.Collection(clark, "e0b0e2920bfec2e1e0a2ffa6ce10")
rows = myCol.getItems()

# Iterate through rows and display them
for row in rows:
    print row
```

### MQTT Messaging
Every system has a **Messaging** client you can use to communicate between devices using the MQTT protocol. To become an MQTT client, all you need is an authenticated user (or device, or developer). If your MQTT broker uses a different port from the default (1883), you can set it with the optional second parameter `port`. The default keep-alive time is 30 seconds, but you can change that with the optional third parameter `keepalive`. Lastly, if your broker lives at a different url than your system, you can specify that with the optional fourth parameter `url`. 

> Definition: `System.Messaging(user, port=1883, keepalive=30, url="")`   
> Returns: MQTT Messaging object.

There are a slew of callback functions you may assign. Typically, you want to set these callbacks before you connect to the broker. This is a list of the function names and their expected parameters:   
- `on_connect(client, userdata, flags, rc)`   
- `on_disconnect(client, userdata, rc)`   
- `on_subscribe(client, userdata, mid, granted_qos)`   
- `on_unsubscribe(client, userdata, mid)`   
- `on_publish(client, userdata, mid)`   
- `on_message(client, userdata, mid)`   
- `on_log(client, userdata, level, buf)`   

Before publishing or subscribing, you must connect your client to the broker. After you're finished, it's good practice to disconnect from the broker before quitting your program. These are both simple functions that take no parameters.

> Definition: `Messaging.connect()`   
> Returns: Nothing.   
> Definition: `Messaging.disconnect()`   
> Returns: Nothing.   

You can subscribe to as many channels as you like, and subsequently unsubscribe from them, using the following two commands. 

> Definition: `Messaging.subscribe(channel)`   
> Returns: Nothing.   
> Definition: `Messaging.unsubscribe(channel)`   
> Returns: Nothing.

{{publish definition here}}

> Definition: `Messaging.publish(channel, message)`   
> Returns: Nothing.

##### Examples


### Code Services



### Queries

