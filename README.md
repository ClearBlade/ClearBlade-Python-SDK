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

`from clearblade.ClearBladeCore import System, Query, Developer`

System, Query, and Developer are the only three classes you should ever need to import directly into your project, however Query and Developer are only used in special situations. 

### Systems
On the ClearBlade platform, you develop IoT solutions through **Systems**. Systems are identified by their SystemKey and SystemSecret. These are the only two parameters needed to work with your system. 

By default, we assume your system lives on our public domain: "https://platform.clearblade.com". If your system lives elsewhere, you can pass the url as the optional third parameter named `url`.

Also by default, we automatically log out any users you authenticate when your script exits. We wrote it this way to reduce the number of user tokens being produced from running a script repeatedly. However, we realize that there are legitimate use cases of wanting to keep users logged in. You can turn off this functionality by passing the boolean `False` as the optional fourth parameter named `safe`.

Definition: `System(systemKey, systemSecret, url="https://platform.clearblade.com", safe=True)`

##### Examples
A regular system on the ClearBlade platform.

```python
from clearblade.ClearBladeCore import System

SystemKey = "9abbd2970baabf8aa6d2a9abcc47"
SystemSecret = "9ABBD2970BA6AABFE6E8AEB8B14F"

mySystem = System(SystemKey, SystemSecret)
```
A system hosted on mydomain.clearblade.com with the auto-logout disabled.

```python
from clearblade.ClearBladeCore import System

SystemKey = "9abbd2970baabf8aa6d2a9abcc47"
SystemSecret = "9ABBD2970BA6AABFE6E8AEB8B14F"
url = "https://mydomain.clearblade.com"

mySystem = System(SystemKey, SystemSecret, url, safe=False)
```

### Users
Within your System, you may have user accounts that can perform actions. Users can be authenticated with their email and password. You may also allow for people to authenticate to your system anonymously. In this case, no email or password is needed. 

Regular user definition: `System.User(email, password)`

Anonymous user definition: `System.AnonUser()`

If you allow users to register new user accounts, we have a method for that too. You need to first authenticate as a user that has the permissions to do so using one of the functions defined above. Then you can register a new user with their email and password. Note that this authenticated user may also be a device or developer.

Defininition: `System.registerUser(authenticatedUser, email, password)`

##### Examples
Authenticating a user.

```python
from clearblade.ClearBladeCore import System

SystemKey = "9abbd2970baabf8aa6d2a9abcc47"
SystemSecret = "9ABBD2970BA6AABFE6E8AEB8B14F"

mySystem = System(SystemKey, SystemSecret)

email = "rob@clearblade.com"
password = "bieberboy"

# Auth as Rob
rob = mySystem.User(email, password)
```
Using an anonymous user to register a new user.

```python
from clearblade.ClearBladeCore import System

SystemKey = "9abbd2970baabf8aa6d2a9abcc47"
SystemSecret = "9ABBD2970BA6AABFE6E8AEB8B14F"

mySystem = System(SystemKey, SystemSecret)

# Auth as anon
anon = mySystem.AnonUser()

# Use the anon user to register Martin
martin = mySystem.registerUser(anon, "martin@clearblade.com", "c00lk1d")
```

### Devices


















